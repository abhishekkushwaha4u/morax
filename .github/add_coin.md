---
name: Add support for a crypto asset
title: ''
labels: feature
assignees: ''

---

## Add support for a new coin

Adding support for a crypto asset is pretty simple.

1. Create a compatible ASCII art for desired coin as a txt file.
2. To enable colours, use seperators like {C1}, {C2}, ..., {Cn}. 
   * It is to be noted that {C1} would substitute the ANSI colour code for the primary colour and {C2} substitute the ANSI colour code for white and so on.
   * {C2} is to always be set to white.
   * Ex. '{c1}abcd{c2}efgh' would render 'abcd' in the colour {C1} and 'efgh' in the colour white.
3. Under 'data/assets/', paste this txt file.
4. Head over to 'data/view.py' and define a funtion for the desired coin.
5. You can take reference from previous definitions.

## Thoroughly test before submitting a pull request.