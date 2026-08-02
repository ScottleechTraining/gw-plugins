# Open-licensed default fonts; commercial fonts stay buyer-supplied

The internal `ig-carousel` skill base64-embeds Vitesse Bold (a commercial Klim Type Foundry font) into every carousel and into `assets/vitesse-bold-base64.txt`. A white-label product that is given away or sold cannot redistribute Vitesse — that violates the foundry license, and the exposure is worse for a paid product.

Decision: the Engine ships Roboto Slab (Apache 2.0) as the default display face and Barlow (OFL) as the default body face, both freely redistributable. Fonts become a Brand Profile slot — buyers may supply their own licensed fonts, and the license for any buyer-supplied font is the buyer's responsibility, stated plainly in the product. Scott's Vitesse exists only in his private Brand Profile and is never shipped in the distributed package.
