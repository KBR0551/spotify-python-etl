-- Table: public.artist_details

-- DROP TABLE IF EXISTS public.artist_details;

CREATE TABLE IF NOT EXISTS public.artist_details
(
    artist_id character varying(30) COLLATE pg_catalog."default" NOT NULL,
    artist_name character varying(50) COLLATE pg_catalog."default",
    followers integer,
    popularity integer,
    CONSTRAINT artist_details_pkey PRIMARY KEY (artist_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.artist_details
    OWNER to postgres;

-- Table: public.artist_albums

-- DROP TABLE IF EXISTS public.artist_albums;

CREATE TABLE IF NOT EXISTS public.artist_albums
(
    album_id character varying(30) COLLATE pg_catalog."default" NOT NULL,
    album_name character varying(150) COLLATE pg_catalog."default",
    artist_id character varying(30) COLLATE pg_catalog."default" NOT NULL,
    total_tracks integer,
    release_date date,
    CONSTRAINT artist_albums_pkey PRIMARY KEY (album_id, artist_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.artist_albums
    OWNER to postgres;

-- Table: public.album_tracks

-- DROP TABLE IF EXISTS public.album_tracks;

CREATE TABLE IF NOT EXISTS public.album_tracks
(
    track_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    track_name character varying(150) COLLATE pg_catalog."default",
    album_id character varying(30) COLLATE pg_catalog."default" NOT NULL,
    track_time numeric(5,2),
    CONSTRAINT album_tracks_pkey PRIMARY KEY (track_id, album_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.album_tracks
    OWNER to postgres;