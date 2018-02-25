.. _quickstart:

.. Quickstart
   ----------

クイックスタート
-------------------

プロジェクトを始めるには、プロジェクトのルートで以下を実行します。
全てのコマンドは、サブコマンドとしてプロジェクトのキーを指定する必要があります。
ここでは、プロジェクト名は `sample` として以下説明していきます。::

    $ revision sample init

これを実行すると、以下のコンフィグファイルが作成されます。

    .revision/config.json
    .revision/sample_revisions.md

`.revision/sample_revisions.md` はオープンソースプロジェクトでよく見かける `CHANGELOG.md` と同じような
フォーマットなので、そのまま公開することも可能です。
