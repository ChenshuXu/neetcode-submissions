# Shopping Cart Service

基于 [2026-09-14 Tessera Labs 面试复盘](../../../../projects/context/Interview/tessera-labs/tessera-labs-software-engineer-backend-interview-debrief-2026-09-14.md)
完成的辅助练习实现。原题要求复用给定的 `ProductService`、`UserService`，
实现加购、读取购物车和结账，允许自行设计签名与返回类型。
下述细节是本地固定的实现约定，不代表面试官规定了唯一答案。

## 接口约定

内部状态保持 `user_id -> product_id -> count`，每个用户的购物车独立。
给定模型和服务保持原样。

| 方法 | 成功返回 | 失败 |
| --- | --- | --- |
| `add_to_cart(user_id, product_id)` | `True`，每次增加一件 | 用户或商品不存在、累计数量超过当前库存时抛 `ValueError` |
| `get_cart(user_id)` | `CartSummary(items, total_price)`；合法空车返回空列表和零金额 | 用户不存在或车内商品已从目录移除时抛 `ValueError` |
| `checkout(user_id)` | `OrderSummary(items, total_price)`；扣除库存并清空该用户购物车 | 无效用户、空车、商品不存在或任一商品库存不足时抛 `ValueError`，库存和购物车均不变 |

- 加购不扣除或预留库存；结账重新检查所有商品，允许数量刚好等于库存。
- `CartItem(product, count)` 分开表达购买数量与库存；`product` 是目录商品的副本。
- 读取时保留缺货商品及其请求数量，并展示当前库存，不静默跳过或减少数量。
- 总价使用当前目录价格乘数量，通过 `Decimal(str(price))` 累加；为兼容给定
  `Product.price: float`，总价返回 `float`。订单保留成交时的商品、数量与价格副本。
- 单线程、内存实现；验证后统一扣库的保证基于给定服务的同步行为，不覆盖并发或外部服务故障。
- 加购平均 O(1) 时间；读取和结账 O(k) 时间、O(k) 输出空间，k 为当前车内商品种类数。

## 运行

从仓库根目录执行：

```bash
python3 custom_practice/tessera_labs/shopping_cart/shopping_cart.py
python3 custom_practice/tessera_labs/shopping_cart/run_tests.py
```

测试复用[共享 runner](../../runner.py)，支持 `--list` 和 `--case`。
覆盖正常金额及数量、累计库存上限、用户隔离、库存变化后整单失败且状态不变、
无效用户/商品，以及重复结账、快照隔离、当前价格和失败后重试。
这些是本地回归检查，不是官方隐藏测试，也不证明限时独立完成能力。
