import todo


if __name__ == "__main__":
    # init db, load ui, + - add task,
    # when task focused - set status: active, inactive, done, remove
    # tasks saved in db sqlite
    app = todo.Todo()
    app.run()
