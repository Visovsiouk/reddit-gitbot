import firebase_admin
import os
import praw
import re
import time

from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

cred = credentials.Certificate("./firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
comments_ref = db.collection(u'comments').document(u'commented')

reddit = praw.Reddit(client_id=os.getenv("REDDIT_ID"),
                     client_secret=os.getenv("REDDIT_SECRET_KEY"),
                     password=os.getenv("REDDIT_PASSWORD"),
                     username=os.getenv("REDDIT_USER_NAME"),
                     user_agent=os.getenv("REDDIT_DESCRIPTION"))

communication_interval = float(os.getenv("COMMUNICATION_INTERVAL"))
limit = int(os.getenv("SUBMISSIONS_LIMIT"))
regexp = re.compile("git(.*)$")
start_time = time.time()
valid_commands = [
    "version", "config", "help", "init", "clone", "add", "status", "diff", "commit", "reset", "rm", "mv", "branch", "checkout", "merge", "mergetool", "log", "stash", "tag", "worktree", "fetch", "pull", "push", "remote", "submodule", "show", "log", "diff", "shortlog", "describe", "Patching", "apply", "cherry-pick", "diff", "rebase", "revert", "Debugging", "bisect", "blame", "grep", "am", "apply", "format-patch", "send-email", "request-pull", "svn", "fast-import", "clean", "gc", "fsck", "reflog", "filter-branch", "instaweb", "archive", "bundle", "Server Admin", "daemon", "update-server-info", "cat-file", "check-ignore", "checkout-index", "commit-tree", "count-objects", "diff-index", "for-each-ref", "hash-object", "ls-files", "ls-tree", "merge-base", "read-tree", "rev-list", "rev-parse", "show-ref", "symbolic-ref", "update-index", "update-ref", "verify-pack", "write-tree"
]

while True:
    comments = comments_ref.get().to_dict()

    for submission in reddit.subreddit('all').top(limit=limit):
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            comment = top_level_comment
            if comment.body:
                command = regexp.search(comment.body)
                if command is not None:
                    command = command.group(1).split()[0]
                    if not command in valid_commands and not comment.id in comments:
                        reply = "git: '" + command + "' is not a git command. See 'git --help'."
                        comment.reply(reply)
                        comments_ref.set({
                            u''+ comment.id + '': comment.body
                        }, merge=True)
    time.sleep(communication_interval - ((time.time() - start_time) % communication_interval))