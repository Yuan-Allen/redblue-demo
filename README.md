# RedBlue Demo
This repository is a demo implementation of RedBlue consistency, which is inspired by [this paper](https://www.usenix.org/system/files/conference/osdi12/osdi12-final-162.pdf).

## Usage
To run the server, use the following command:
```
./scripts/start_server.sh
```

To run the command client, use the following command:
```
./scripts/start_cmd_client.sh {{address}}
# for example, ./scripts/start_cmd_client.sh http://localhost:13000
```

To run the simple test client, use the following command:
```
./scripts/start_test_client.sh
```

