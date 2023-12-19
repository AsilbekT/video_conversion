from app.database.connection import SessionLocal
from app.models.content import Movie, Series, Episode
from credentials import PLAYBACK_SERVICE


def update_content_url(content_id: int, hls_path: str, url_type: str):
    db = SessionLocal()

    content_model = get_content_model(url_type)
    if not content_model:
        db.close()
        return None

    content = db.query(content_model).filter(
        content_model.id == content_id).first()
    if content:
        if url_type == "MOVIE":
            content.main_content_url = PLAYBACK_SERVICE + hls_path
            content.is_ready = True
        elif url_type == "SERIES":
            content.series_summary_url = PLAYBACK_SERVICE + hls_path
            content.is_ready = True
        elif url_type == "EPISODE":
            content.episode_content_url = PLAYBACK_SERVICE + hls_path
            content.is_ready = True
        elif url_type in ["MOVIE_TRAILER", "SERIES_TRAILER"]:
            content.trailer_url = PLAYBACK_SERVICE + hls_path
            content.has_trailer = True

        else:
            db.close()
            return None

        db.commit()
        db.refresh(content)
        db.close()
        return content
    else:
        db.close()
        return None


def content_exists(content_id: int, content_type: str):
    db = SessionLocal()

    content_model = get_content_model(content_type)
    if not content_model:
        db.close()
        return False

    content = db.query(content_model).filter(
        content_model.id == content_id).first()
    db.close()
    return content is not None


def get_content_model(content_type: str):
    content_types = {
        "MOVIE": Movie,
        "SERIES": Series,
        "EPISODE": Episode,
        "MOVIE_TRAILER": Movie,  # Assuming trailers have the same model as movies
        "SERIES_TRAILER": Series  # Assuming trailers have the same model as series
    }

    return content_types.get(content_type.upper())
