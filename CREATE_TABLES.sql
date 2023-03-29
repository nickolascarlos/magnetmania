CREATE TABLE media (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255),
  ano INTEGER
);

CREATE TABLE media_metadata (
  media_id INT REFERENCES media(id) ON DELETE CASCADE,
  property VARCHAR(255),
  value VARCHAR(2048)
);

CREATE TABLE magnet (
  hash VARCHAR(255) PRIMARY KEY,
  media_id INT REFERENCES media(id)
);

CREATE TABLE magnet_metadata (
  magnet_id VARCHAR(255) REFERENCES magnet(hash) ON DELETE CASCADE,
  property VARCHAR(255),
  value VARCHAR(2048)
);