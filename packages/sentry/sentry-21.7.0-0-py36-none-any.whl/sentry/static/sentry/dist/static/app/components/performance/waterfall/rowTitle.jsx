Object.defineProperty(exports, "__esModule", { value: true });
exports.RowTitleContent = exports.RowTitle = exports.RowTitleContainer = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var constants_1 = require("app/components/performance/waterfall/constants");
exports.RowTitleContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: ", "px;\n  position: absolute;\n  left: 0;\n  top: 0;\n  width: 100%;\n  user-select: none;\n"], ["\n  display: flex;\n  align-items: center;\n  height: ", "px;\n  position: absolute;\n  left: 0;\n  top: 0;\n  width: 100%;\n  user-select: none;\n"])), constants_1.ROW_HEIGHT);
exports.RowTitle = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  height: 100%;\n  font-size: ", ";\n  white-space: nowrap;\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  position: relative;\n  height: 100%;\n  font-size: ", ";\n  white-space: nowrap;\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeSmall; });
exports.RowTitleContent = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return (p.errored ? p.theme.error : 'inherit'); });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=rowTitle.jsx.map