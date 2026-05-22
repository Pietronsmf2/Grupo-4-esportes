-- =============================================
--  MOTION CLUB — Schema do Banco de Dados
--  Sprint 5 · Modelagem relacional
-- =============================================
 
-- Extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
 
-- -----------------------------------------------
-- TABELA: users
-- -----------------------------------------------
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    uuid        UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,       -- hash bcrypt
    bio         TEXT,
    avatar_url  VARCHAR(500),
    is_active   BOOLEAN DEFAULT TRUE,
    is_admin    BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP DEFAULT NOW()
);
 
-- -----------------------------------------------
-- TABELA: sports (modalidades)
-- -----------------------------------------------
CREATE TABLE sports (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,  -- ex: 'Futebol'
    slug        VARCHAR(100) UNIQUE NOT NULL,  -- ex: 'futebol'
    emoji       VARCHAR(10),
    created_at  TIMESTAMP DEFAULT NOW()
);
 
-- -----------------------------------------------
-- TABELA: user_sports (esportes do usuário)
-- -----------------------------------------------
CREATE TABLE user_sports (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sport_id    INTEGER NOT NULL REFERENCES sports(id) ON DELETE CASCADE,
    skill_level VARCHAR(20) DEFAULT 'iniciante' CHECK (skill_level IN ('iniciante','intermediario','avancado')),
    UNIQUE(user_id, sport_id)
);
 
-- -----------------------------------------------
-- TABELA: events (partidas/eventos)
-- -----------------------------------------------
CREATE TABLE events (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    description     TEXT,
    sport_id        INTEGER REFERENCES sports(id),
    organizer_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    location        VARCHAR(300),
    latitude        DECIMAL(9,6),
    longitude       DECIMAL(9,6),
    scheduled_at    TIMESTAMP NOT NULL,
    max_players     INTEGER DEFAULT 10,
    status          VARCHAR(20) DEFAULT 'aberto' CHECK (status IN ('aberto','cheio','encerrado','cancelado')),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
 
-- -----------------------------------------------
-- TABELA: event_participants (confirmações de presença)
-- -----------------------------------------------
CREATE TABLE event_participants (
    id              SERIAL PRIMARY KEY,
    event_id        INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status          VARCHAR(20) DEFAULT 'confirmado' CHECK (status IN ('confirmado','pendente','cancelado')),
    confirmed_at    TIMESTAMP DEFAULT NOW(),
    UNIQUE(event_id, user_id)
);
 
-- -----------------------------------------------
-- TABELA: reviews (avaliações de usuários)
-- -----------------------------------------------
CREATE TABLE reviews (
    id              SERIAL PRIMARY KEY,
    reviewer_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reviewed_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_id        INTEGER REFERENCES events(id) ON DELETE SET NULL,
    rating          SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment         TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(reviewer_id, reviewed_id, event_id)
);
 
-- -----------------------------------------------
-- TABELA: badges (conquistas)
-- -----------------------------------------------
CREATE TABLE badges (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(300),
    icon        VARCHAR(100),
    criteria    VARCHAR(300)  -- ex: 'Participou de 10 partidas'
);
 
CREATE TABLE user_badges (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id    INTEGER NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
    earned_at   TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, badge_id)
);
 
-- -----------------------------------------------
-- TABELA: plans (planos de apoio)
-- -----------------------------------------------
CREATE TABLE plans (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    price       DECIMAL(10,2) NOT NULL,
    interval    VARCHAR(20) DEFAULT 'monthly' CHECK (interval IN ('monthly','yearly')),
    description TEXT,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT NOW()
);
 
-- -----------------------------------------------
-- TABELA: supports (apoios/assinaturas)
-- -----------------------------------------------
CREATE TABLE supports (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id         INTEGER NOT NULL REFERENCES plans(id),
    status          VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','cancelled','expired')),
    started_at      TIMESTAMP DEFAULT NOW(),
    expires_at      TIMESTAMP,
    stripe_sub_id   VARCHAR(200)  -- ID da assinatura no Stripe
);
 
-- -----------------------------------------------
-- Índices para performance
-- -----------------------------------------------
CREATE INDEX idx_events_sport_id ON events(sport_id);
CREATE INDEX idx_events_organizer_id ON events(organizer_id);
CREATE INDEX idx_events_scheduled_at ON events(scheduled_at);
CREATE INDEX idx_event_participants_event_id ON event_participants(event_id);
CREATE INDEX idx_event_participants_user_id ON event_participants(user_id);
CREATE INDEX idx_user_sports_user_id ON user_sports(user_id);
CREATE INDEX idx_reviews_reviewed_id ON reviews(reviewed_id);
 
