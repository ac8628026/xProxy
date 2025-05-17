from sqlalchemy.orm import Session
from db.dbconfig import session
from .models import Mention

def push_mentions(mention_id,parent_text, mention_text,timestamp ,mention_url,replied,replied_at,reply):
    sessiondb = session()
    try:
        new_mention = Mention(
            id = mention_id,
            mention_text = mention_text,
            parent_text = parent_text,
            mention_url = mention_url,
            timestamp=timestamp,
            replied = replied,
            replied_at = replied_at,
            reply = reply
        )
        # print(f"mentioning data : {new_mention}")
        sessiondb.add(new_mention)
        sessiondb.commit()
        # print("Mention pushed")
    except Exception as e:
        sessiondb.rollback()
        print(" Error during mention pushing",e)

    finally:
        sessiondb.close()

def update_mention_reply(mention_id,replied,replied_at,reply):
    sessiondb = session()
    try:
        mention = sessiondb.query(Mention).filter(Mention.id == mention_id).first()
        if mention:
            mention.replied = replied
            mention.replied_at = replied_at
            mention.reply = reply
            sessiondb.commit()
    except Exception as e:
        sessiondb.rollback()
        print(" Error during mention updating",e)

    finally:
        sessiondb.close()