## Abstract

This package consists of the following modules:
- [IntegralMath](#integralmath) - a set of functions, each of which returning an integer result
- [FractionMath](#fractionmath) - a set of functions, each of which returning a rational result
- [AnalyticMath](#analyticmath) - a set of exponential and logarithmic functions
- [AdvancedMath](#advancedmath) - a function for solving xA^x = B, given rational values of A and B
- [BodningCurve](#bodningcurve) - a set of functions implementing the bonding-curve mechanism
- [DynamicCurve](#dynamiccurve) - a function for equalizing the weights in a bonding-curve model

### Class Hierarchy
```
IntegralMath < - - - - FractionMath
      ∧                      ∧
      |                      |
      |                      |
      |                      |
AnalyticMath < - - - - AdvancedMath
      ∧                      ∧
      |                      |
      |                      |
      |                      |
BodningCurve           DynamicCurve
```

Note that some of these modules are implemented as `library`, while others are implemented as `contract`.

Nevertheless, they can all be regarded as *libraries*, since the reason for this is purely technical.

A library cannot utilize non-constant state variables, nor can it extend (inherit) another library.

<br/><br/>

---

<br/><br/>

## IntegralMath

This module implements the following interface:
- `function floorLog2(uint256 n)` => `(uint8)`
- `function floorSqrt(uint256 n)` => `(uint256)`
- `function ceilSqrt(uint256 n)` => `(uint256)`
- `function floorCbrt(uint256 n)` => `(uint256)`
- `function ceilCbrt(uint256 n)` => `(uint256)`
- `function roundDiv(uint256 n, uint256 d)` => `(uint256)`
- `function mulDivF(uint256 x, uint256 y, uint256 z)` => `(uint256)`
- `function mulDivC(uint256 x, uint256 y, uint256 z)` => `(uint256)`

Function `floorLog2(n)` computes the largest integer smaller than or equal to the binary logarithm of `n`.

Function `floorSqrt(n)` computes the largest integer smaller than or equal to the square root of `n`.

Function `ceilSqrt(n)` computes the smallest integer larger than or equal to the square root of `n`.

Function `floorCbrt(n)` computes the largest integer smaller than or equal to the cubic root of `n`.

Function `ceilCbrt(n)` computes the smallest integer larger than or equal to the cubic root of `n`.

Function `roundDiv(n, d)` computes the nearest integer to the quotient of `n` and `d` (or `n / d`).

Function `mulDivF(x, y, z)` computes the largest integer smaller than or equal to `x * y / z`.

Function `mulDivC(x, y, z)` computes the smallest integer larger than or equal to `x * y / z`.

Note that function `mulDivF` and function `mulDivC` revert when the **actual** result is larger than 256 bits.

Note that function `floorSqrt` and function `ceilSqrt` are guaranteed to return the correct output for every input.

However, when compared with the **actual** square root, smaller input generally yields relatively lower accuracy of the output.

For example, `floorSqrt(3)` returns 1, but the actual square root of 3 is ~1.73, which yields a relative accuracy of only ~57%.

Note that function `floorCbrt` and function `ceilCbrt` are guaranteed to return the correct output for every input.

However, when compared with the **actual** cubic root, smaller input generally yields relatively lower accuracy of the output.

For example, `floorCbrt(7)` returns 1, but the actual cubic root of 7 is ~1.91, which yields a relative accuracy of only ~52%.

<br/><br/>

---

<br/><br/>

## FractionMath

This module implements the following interface:
- `function normalizedRatio(uint256 n, uint256 d, uint256 scale)` => `(uint256, uint256)`
- `function reducedRatio(uint256 n, uint256 d, uint256 max)` => `(uint256, uint256)`
- `function productRatio(uint256 n1, uint256 n2, uint256 d1, uint256 d2)` => `(uint256, uint256)`
- `function poweredRatio(uint256 n, uint256 d, uint256 exp, bool fast)` => `(uint256, uint256)`

### Normalized Ratio

Function `normalizedRatio` computes the nearest ratio whose sum of components (numerator + denominator) equals the input scale.

Note that the output ratio can be larger than the input ratio in some cases, and smaller than the input ratio in other cases.

For example:
- `normalizedRatio(12, 34, 100)` returns `(26 74)`; the output ratio is smaller than the input ratio (26 / 74 = 0.351 < 0.352 = 12 / 34)
- `normalizedRatio(1234, 5678, 100)` returns `(18 82)`; the output ratio is larger than the input ratio (18 / 82 = 0.219 > 0.217 = 1234 / 5678)

Keep in mind that it is an important consideration to take when choosing to use this function.

For example, when designing a sustainable financial model, it is imperative to never entitle more than the actual entitlement.

The same consideration applies for all the other functions in this module, since each one of them uses this function internally.

### Reduced Ratio

Function `reducedRatio` computes the nearest ratio whose components (numerator and denominator) are not larger than the input threshold.

Internally, it calls function `normalizedRatio` with the input threshold, but only if one of the components is larger than that threshold.

Note that function `reducedRatio` is not meant to replace GCD, nor does it strive to achieve better accuracy.

GCD is not being used here, because the time-complexity of this method depends on the bit-length of the input.

The worst case is when the two input valus are consecutive Fibonacci numbers, in the case of `uint256` - F369 and F370, which yield 367 iterations.

Moreover, the main issue with using GCD for reducing an arbitrary ratio, is the fact that it doesn't even guarantee the desired reduction to begin with.

Reducing an input ratio by its GCD in advance (at your own expense) can most certainly improve the output of function `reducedRatio` in terms of accuracy.

However, without knowing specific characteristics of that ratio (e.g., each one of its components is a multiple of `0x1000`), doing so is generally useless.

### Product Ratio

Function `productRatio` computes the product of two ratios as a single ratio whose components are not larger than 256 bits.

If either one of the intermediate components is larger than 256 bits, then both of them are reduced based on the larger one.

### Powered Ratio

Function `poweredRatio` computes the power of a given ratio by a given exponent.

In order to avoid multiplication overflow, it may truncate the intermediate result on each iteration.

Subsequently, the larger the input exponent is, the lower the accuracy of the output is likely to be.

The input argument `fast` allows to opt for either accuracy (using `false`) or performance (using `true`).

This library defines a maximum exponent of 4 bits (i.e., 15), which can be customized to fit the system requirements.

<br/><br/>

---

<br/><br/>

## AnalyticMath

This module is implemented as a contract, because a library cannot utilize non-constant state variables.

It implements the following interface:
- `function pow(uint256 a, uint256 b, uint256 c, uint256 d)` => `(uint256, uint256)`
- `function log(uint256 a, uint256 b)` => `(uint256, uint256)`
- `function exp(uint256 a, uint256 b)` => `(uint256, uint256)`

### Initialization

Prior to using any of these functions, internal data structure must be initialized by executing function `init`.

Function `init` should be executed either during construction or after construction (if too large for the constructor).

Thus, any contract which inherits this contract can choose whether or not to call function `init` in its constructor.

### Exponentiation

Function `pow(a, b, c, d)` approximates the power of `a / b` by `c / d`.

When `a >= b`, the output of this function is guaranteed to be smaller than or equal to the actual value of (a / b) ^ (c / d).

When `a <= b`, the output of this function is guaranteed to be larger than or equal to the actual value of (a / b) ^ (c / d).

### Natural Logarithm

Function `log(a, b)` approximates the natural logarithm of `a / b`.

The output of this function is guaranteed to be smaller than or equal to the actual value of log(a / b).

It does not support `a < b`, because it relies on unsigned-integer arithmetic, and the output for such input would be negative.

### Natural Exponentiation

Function `exp(a, b)` approximates the natural exponentiation of `a / b`.

The output of this function is guaranteed to be smaller than or equal to the actual value of exp(a / b).

### Contract Customization

This contract can be customized to support different input ranges (as a tradeoff with accuracy and/or performance).

The full customization manual can be found [here](#customization).

<br/><br/>

---

<br/><br/>

## AdvancedMath

This module is implemented as a contract, because a library cannot utilize non-constant state variables.

It implements the following interface:
- `function solve(uint256 a, uint256 b, uint256 c, uint256 d)` => `(uint256, uint256)`

### Initialization

Prior to using any of these functions, internal data structure must be initialized by executing function `init`.

Function `init` should be executed either during construction or after construction (if too large for the constructor).

Thus, any contract which inherits this contract can choose whether or not to call function `init` in its constructor.

### Equation Solving

Function `solve(a, b, c, d)` computes a value of x which satisfies the equation x * (a / b) ^ x = c / d.

A detailed description of how this function works can be found [here](readme/AdvancedMath.pdf).

### Contract Customization

This contract can be customized to support different input ranges (as a tradeoff with accuracy and/or performance).

The full customization manual can be found [here](#customization).

<br/><br/>

---

<br/><br/>

## BodningCurve

This module is implemented as a contract, because a library cannot extend (inherit) a contract.

It implements the following interface:
- `function buy(uint256 supply, uint256 balance, uint256 weight, uint256 amount)` => `(uint256)`
- `function sell(uint256 supply, uint256 balance, uint256 weight, uint256 amount)` => `(uint256)`
- `function convert(uint256 balance1, uint256 weight1, uint256 balance2, uint256 weight2, uint256 amount)` => `(uint256)`
- `function deposit(uint256 supply, uint256 balance, uint256 weights, uint256 amount)` => `(uint256)`
- `function withdraw(uint256 supply, uint256 balance, uint256 weights, uint256 amount)` => `(uint256)`
- `function invest(uint256 supply, uint256 balance, uint256 weights, uint256 amount)` => `(uint256)`

### Initialization

Prior to using any of these functions, internal data structure must be initialized by executing function `init`.

Function `init` should be executed either during construction or after construction (if too large for the constructor).

Thus, any contract which inherits this contract can choose whether or not to call function `init` in its constructor.

### Functionality

```
|----------------------------|--------------------------------------------------|---------------------------------------------|
| Function                   | Compute the return of                            | Formula                                     |
|----------------------------|--------------------------------------------------|---------------------------------------------|
| buy(s, b, w, x)            | buying pool tokens with reserve tokens           | s * ((1 + x / b) ^ (w / MAX_WEIGHT) - 1)    |
| sell(s, b, w, x)           | selling pool tokens for reserve tokens           | b * (1 - (1 - x / s) ^ (MAX_WEIGHT / w))    |
| convert(b1, w1, b2, w2, x) | converting reserve tokens of one type to another | b2 * (1 - (b1 / (b1 + x)) ^ (w1 / w2))      |
| deposit(s, b, ws, x)       | depositing reserve tokens for pool tokens        | s * ((x / b + 1) ^ (ws / MAX_WEIGHT) - 1)   |
| withdraw(s, b, ws, x)      | withdrawing reserve tokens with pool tokens      | b * (1 - ((s - x) / s) ^ (MAX_WEIGHT / ws)) |
| invest(s, b, ws, x)        | investing reserve tokens for pool tokens         | b * (((s + x) / s) ^ (MAX_WEIGHT / ws) - 1) |
|----------------------------|--------------------------------------------------|---------------------------------------------|
```

The bonding-curve model was conceived by [Bancor](https://github.com/bancorprotocol).

<br/><br/>

---

<br/><br/>

## DynamicCurve

This module is implemented as a contract, because a library cannot extend (inherit) a contract.

It implements the following interface:
- `function equalize(uint256 t, uint256 s, uint256 r, uint256 q, uint256 p)` => `(uint256, uint256)`

### Initialization

Prior to using any of these functions, internal data structure must be initialized by executing function `init`.

Function `init` should be executed either during construction or after construction (if too large for the constructor).

Thus, any contract which inherits this contract can choose whether or not to call function `init` in its constructor.

### Equalization

Consider a pool which implements the bonding-curve model over a primary reserve token and a secondary reserve token.

Let 'on-chain price' denote the conversion rate between these tokens inside the pool (i.e., as determined by the pool).

Let 'off-chain price' denote the conversion rate between these tokens outside the pool (i.e., as determined by the market).

The arbitrage incentive is always to convert to the point where the on-chain price is equal to the off-chain price.

We want this operation to also impact the primary reserve balance becoming equal to the primary reserve staked balance.

In other words, we want the arbitrager to convert the difference between the reserve balance and the reserve staked balance.

Hence we adjust the weights in order to create an arbitrage incentive which, when realized, will subsequently equalize the pool.

Input:
- Let t denote the primary reserve token staked balance
- Let s denote the primary reserve token balance
- Let r denote the secondary reserve token balance
- Let q denote the numerator of the off-chain price
- Let p denote the denominator of the off-chain price

Where p primary tokens are equal to q secondary tokens

Output:
- Solve the equation x * (s / t) ^ x = (t / r) * (q / p)
- Return x / (x + 1) as the weight of the primary reserve token
- Return 1 / (x + 1) as the weight of the secondary reserve token

A detailed reasoning of this method can be found [here](readme/DynamicCurve.pdf).

If the rate-provider provides the rates for a common unit, for example:
- P = 2 ==> 2 primary reserve tokens = 1 ether
- Q = 3 ==> 3 secondary reserve tokens = 1 ether

Then you can simply use p = P and q = Q

If the rate-provider provides the rates for a single unit, for example:
- P = 2 ==> 1 primary reserve token = 2 ethers
- Q = 3 ==> 1 secondary reserve token = 3 ethers

Then you can simply use p = Q and q = P

The dynamic-curve method was conceived by [Bancor](https://github.com/bancorprotocol).

<br/><br/>

---

<br/><br/>

## Testing

### Prerequisites

- `node 12.20.0`
- `yarn 1.22.10` or `npm 7.12.0`

### Installation

- `yarn install` or `npm install`

### Compilation

- `yarn build` or `npm run build`

### Execution

- `yarn test` or `npm run test`

### Verification

- `yarn verify` or `npm run verify`

<br/><br/>

---

<br/><br/>

## Emulation

### Prerequisites

- `python 3.9`

### Execution

In order to allow rapid testing and verification, all modules (contracts and libraries) have been ported from Solidity to Python:
- The emulation modules themselves are located under [FixedPoint](project/emulation/FixedPoint)
- The corresponding floating-point functionality is located under [FloatPoint](project/emulation/FloatPoint)
- A set of unit-tests for various functions (one per function) is located under [emulation](project/emulation)

<br/><br/>

---

<br/><br/>

## Customization

All customization parameters are located in [constants.py](project/emulation/AutoGenerate/common/constants.py).

When modifying **any** of them, one should regenerate **all** the code.

The following scripts generate the code for [AnalyticMath.sol](project/contracts/AnalyticMath.sol):
- [PrintLn2ScalingFactors.py ](project/emulation/AutoGenerate/PrintLn2ScalingFactors.py )
- [PrintOptimalThresholds.py ](project/emulation/AutoGenerate/PrintOptimalThresholds.py )
- [PrintFunctionGeneralExp.py](project/emulation/AutoGenerate/PrintFunctionGeneralExp.py)
- [PrintFunctionOptimalLog.py](project/emulation/AutoGenerate/PrintFunctionOptimalLog.py)
- [PrintFunctionOptimalExp.py](project/emulation/AutoGenerate/PrintFunctionOptimalExp.py)
- [PrintMaxExpArray.py       ](project/emulation/AutoGenerate/PrintMaxExpArray.py       )

The following scripts generate the code for [AdvancedMath.sol](project/contracts/AdvancedMath.sol):
- [PrintLambertFactors.py     ](project/emulation/AutoGenerate/PrintLambertFactors.py     )
- [PrintFunctionLambertNeg1.py](project/emulation/AutoGenerate/PrintFunctionLambertNeg1.py)
- [PrintFunctionLambertPos1.py](project/emulation/AutoGenerate/PrintFunctionLambertPos1.py)
- [PrintLambertArray.py       ](project/emulation/AutoGenerate/PrintLambertArray.py       )

In order to retain the [testing infrastructure](#testing), one should proceed by:
- Running the script [PrintTestConstants.py](project/emulation/AutoGenerate/PrintTestConstants.py)
- Pasting the printout into [AnalyticMathConstants.js](project/tests/helpers/AnalyticMathConstants.js)

In order to retain the [emulation infrastructure](#emulation), one should proceed by:
- Porting all changes from [AnalyticMath.sol](project/contracts/AnalyticMath.sol) to [AnalyticMath.py](project/emulation/FixedPoint/AnalyticMath.py)
- Porting all changes from [AdvancedMath.sol](project/contracts/AdvancedMath.sol) to [AdvancedMath.py](project/emulation/FixedPoint/AdvancedMath.py)
