### Dependecies and Run
```
    (venv) $ pip install fastapi uvicorn[standard]

    (venv) $ uvicorn app:app --reload
```

### Note
Must run "uvicorn app:app" on console to run a script

Running uvicorn in __main__ will fail to run a script

```
        if __name__ == '__main__':
            uvicorn.run(app)
 ```

### References
- https://realpython.com/api-integration-in-python/
- https://stackoverflow.com/questions/62934384/how-to-add-timestamp-to-each-request-in-uvicorn-logs
- https://www.jeffastor.com/blog/designing-a-robust-user-model-in-a-fastapi-app
- https://pydantic-docs.helpmanual.io/usage/validators/