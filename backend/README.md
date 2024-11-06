# バックエンドアプリケーションの起動方法

## 環境構築フロー

1. git cloneを実行

    ```bash
    cd $workspace
    git@github.com:dev-chickenx/backend-todo.git
    ```

## 起動手順

1. docker の起動

    ```bash
    cd ~/$workspace/backend-todo
    docker compose up
    ```

2. docker コンテナとローカル環境の同期（ボリュームマウント）を取らない場合

    ```bash
    cd ~/$workspace/backend-todo
    docker compose -f docker-compose.prod.yaml up
    ```
