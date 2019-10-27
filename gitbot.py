import time
import os
import praw
import re

from dotenv import load_dotenv
load_dotenv()

commented_ids = []

valid_commands = [
    "version", "config", "help", "init", "clone", "add", "status", "diff", "commit", "reset", "rm", "mv", "branch", "checkout", "merge", "mergetool", "log", "stash", "tag", "worktree", "fetch", "pull", "push", "remote", "submodule", "show", "log", "diff", "shortlog", "describe", "Patching", "apply", "cherry-pick", "diff", "rebase", "revert", "Debugging", "bisect", "blame", "grep", "am", "apply", "format-patch", "send-email", "request-pull", "svn", "fast-import", "clean", "gc", "fsck", "reflog", "filter-branch", "instaweb", "archive", "bundle", "Server Admin", "daemon", "update-server-info", "cat-file", "check-ignore", "checkout-index", "commit-tree", "count-objects", "diff-index", "for-each-ref", "hash-object", "ls-files", "ls-tree", "merge-base", "read-tree", "rev-list", "rev-parse", "show-ref", "symbolic-ref", "update-index", "update-ref", "verify-pack", "write-tree"
]

reddit = praw.Reddit(client_id=os.getenv("REDDIT_ID"),
                     client_secret=os.getenv("REDDIT_SECRET_KEY"),
                     password=os.getenv("REDDIT_PASSWORD"),
                     username=os.getenv("REDDIT_USER_NAME"),
                     user_agent=os.getenv("REDDIT_DESCRIPTION"))

start_time=time.time()

regexp = re.compile("git(.*)$")

while True:
    for submission in reddit.subreddit('all').top(limit=os.getenv("SUBMISSIONS_LIMIT")):
        for top_level_comment in submission.comments:
            comment = top_level_comment
            if comment.body:
                command = regexp.search(comment.body)
                if command is not None:
                    command = command.group(1).split()[0]
                    if not command in valid_commands and not comment.id in commented_ids:
                        reply = "git: '" + command + "' is not a git command. See 'git --help'."
                        comment.reply(reply)
                        commented_ids.append(comment.id)
    time.sleep(60.0 - ((time.time() - start_time) % 60.0))