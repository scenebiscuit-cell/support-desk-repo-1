---
title: Integrations
slug: integrations
category: Integrations
---

# Integrations

Pharos connects with Slack, Google Drive, GitHub, Google Calendar, Outlook, and Zapier. Workspace owners and admins manage them under **Settings > Integrations**.

## Slack

Connect Slack to post task updates to a channel and create tasks from Slack messages. After connecting, open a project and choose a channel under **Project settings > Slack**. Each project can post to one channel.

## Google Drive

Attach Drive files to tasks without downloading them. Files keep their Google sharing settings, so people need access in Drive to open them.

## GitHub

Link pull requests and commits to tasks by including the task ID (for example, `PHR-142`) in the branch name, commit message, or pull request title. Linked pull requests show on the task and can move it to *Done* when merged.

## Calendar sync

Connect Google Calendar or Outlook under **Profile > Calendar** to see your tasks' due dates on your calendar. Each person connects their own calendar. Sync runs every 15 minutes.

## An integration stopped working

1. Check **Settings > Integrations**. A red **Reconnect** banner means access expired, often after a password change or when the person who connected it left the workspace. Click **Reconnect** and sign in again.
2. For Slack, make sure the Pharos app is still in the channel. If someone removed it, type `/invite @Pharos` in the channel.
3. For GitHub, check that the repository is still selected under **Settings > Integrations > GitHub > Repositories**.
4. Disconnect and reconnect. Existing links and attachments aren't deleted.

## Still not working?

Contact support with the integration name, the project, and roughly when it stopped. We can check the integration log for your workspace.
