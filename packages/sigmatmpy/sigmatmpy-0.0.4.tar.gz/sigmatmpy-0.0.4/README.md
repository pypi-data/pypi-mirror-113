# SIGMATMPY

> SIGMATMPY-library is an APIRequest driven trading and monitoring platform. Each functionality (trades, price etc.) is represented by it's own class covering all aspect of that functionality.


## Getting Started 使用指南

### Installation 安装

```sh
$ pip install sigmatmpy
```

### Usage example 使用示例

```sh
import sigmatmpy

# initualize APIRequest token
username = 'username'
password = 'password'
API = sigmatmpy.API(username,password)

# open_order(symbol, cmd, volume, price, slippage, stoploss, takeprofit)
API.open_order('EURUSD-STD',1,0.01,1.18245,3,0,0)

# close_order(ticket, volume, price)
API.close_order(2067652,0.01,1.18245)

# trades_user_history(login , start_time, end_time)
API.trades_user_history(99999981, '2021-07-04 000000', '2021-07-16 075150')

# trades_user_history2(login , start_time_ctm, end_time_ctm)
API.trades_user_history(99999981, 1625991769, 1626423769)
```

## Deployment 部署方法

部署到生产环境注意事项。


## Release History 版本历史


## Authors 关于作者

* **SIGMATM** - *Initial work* - [SIGMATM]

查看更多关于这个项目的贡献者，请阅读 [contributors](#) 

## License 授权协议

这个项目 MIT 协议， 请点击 [LICENSE.md](LICENSE.md) 了解更多细节。