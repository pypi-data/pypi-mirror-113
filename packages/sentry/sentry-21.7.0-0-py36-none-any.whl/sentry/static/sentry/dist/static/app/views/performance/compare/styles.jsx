Object.defineProperty(exports, "__esModule", { value: true });
exports.SpanBarRectangle = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var constants_1 = require("app/components/performance/waterfall/constants");
exports.SpanBarRectangle = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  height: ", "px;\n  top: ", "px;\n  min-width: 1px;\n  user-select: none;\n  transition: border-color 0.15s ease-in-out;\n  border-right: 1px solid rgba(0, 0, 0, 0);\n"], ["\n  position: relative;\n  height: ", "px;\n  top: ", "px;\n  min-width: 1px;\n  user-select: none;\n  transition: border-color 0.15s ease-in-out;\n  border-right: 1px solid rgba(0, 0, 0, 0);\n"])), constants_1.ROW_HEIGHT - 2 * constants_1.ROW_PADDING, constants_1.ROW_PADDING);
var templateObject_1;
//# sourceMappingURL=styles.jsx.map