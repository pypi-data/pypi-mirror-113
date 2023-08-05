Object.defineProperty(exports, "__esModule", { value: true });
var utils_1 = require("app/utils");
/**
 * A threshold has a value if it is not one of the following:
 *
 * '', null, undefined
 *
 *
 */
function hasThresholdValue(value) {
    return utils_1.defined(value) && value !== '';
}
exports.default = hasThresholdValue;
//# sourceMappingURL=hasThresholdValue.jsx.map