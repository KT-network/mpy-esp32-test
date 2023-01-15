# mqtt数据格式定义

## esp32 开发板 数据接收格式

#### 各种定义

```
behavior 类型


```

### 控制 单独或多个 Pin 引脚

开发板接收的数据

```json
{
  "behavior": 0,
  "action": {
    "pin": [
      12,
      14,
      27,
      26,
      25,
      33
    ],
    "value": [
      1,
      1,
      1,
      1,
      1,
      1
    ]
  }
}
```

### 修改配置文件NVS

```json
{
  "behavior": 1,
  "action": {
    "NVS": "wifi",
    "value": {},
    "now": true
  }
}
```

| behavior | action | NVS  | value | now  |
|----------|--------|------|-------|------|
| 1        |        | wifi |       | 立即执行 |



