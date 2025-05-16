from scraper.mentions import get_mentions
from redisconfig.cache import check_reply, mark_as_replyed, mark_as_unreplyed
from db.crud import push_mentions, update_mention_reply
from bot.reply_bot import reply_to_tweet
from personalize_reply.get_reply import get_reply_text
import datetime


def x_bot():
    mentions = get_mentions()
    print("successfully get mentions")
    # mentions = [{'id': '1910778685977673840', 'parent_text': 'My ranking for captaincy this IPL season:\n\n1) Shreyas Iyer,\n2) Axar Patel,\n3) Ashish Nehra,\n4) Rajat Patidar,\n5) Sanju Samson,\n6) Ajinkya Rahane,\n7) Hardik Pandya,\n8) Rishabh Pant,\n9) Pat Cummins,\n10) Ruturaj Gaikwad\n\nBasis- Captaincy + Performance. Yours?', 'mention_text': '@AshokCh05268450\n .check is', 'timestamp': '2025-04-11T06:28:34.000Z', 'url': 'https://x.com/Akch86/status/1910778685977673840'}, {'id': '1910778685977673840', 'parent_text': 'Discover tokens, explore real-time data, and make swaps — all in one app. \n\nConnect your wallet to the Uniswap Web app and swap smarter today.', 'mention_text': '', 'timestamp': '2025-04-24T12:29:47.000Z', 'url': 'https://x.com/Akch86/status/1910778685977673840/analytics'}]
    # print(f"mentions : {mentions}")
    for mention in mentions:
        mention_id = mention["id"]
       
        # if check_reply(mention_id):
        #     print(f"continue : {mention_id}")
        #     continue
        ### Already checking while extracting data of every mention


        push_mentions(
            mention_id=mention_id,
            parent_text =mention["parent_text"],
            mention_text=mention["mention_text"],
            timestamp = mention["timestamp"],
            mention_url = mention["url"],
            replied = False,
            replied_at = None,
            reply = None
             )
        print(f"push done")
        # reply_text = " back to you"
        reply_text = get_reply_text(mention["parent_text"],mention["mention_text"])
        result = reply_to_tweet(tweet_id=mention_id, reply_text=reply_text)

        if result:
            print(f"replied with :{mention_id}")
            update_mention_reply(mention_id,replied=True, replied_at=datetime.datetime.now(),reply=reply_text)
            mark_as_replyed(mention_id)

x_bot()