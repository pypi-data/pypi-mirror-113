Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorPanel = exports.DoubleHeaderContainer = exports.GridCellNumber = exports.GridCell = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.GridCell = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 14px;\n"], ["\n  font-size: 14px;\n"])));
exports.GridCellNumber = styled_1.default(exports.GridCell)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
exports.DoubleHeaderContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  padding: ", " ", " ", " ", ";\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  padding: ", " ", " ", " ", ";\n  grid-gap: ", ";\n"])), space_1.default(2), space_1.default(3), space_1.default(1), space_1.default(3), space_1.default(3));
exports.ErrorPanel = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n\n  flex: 1;\n  flex-shrink: 0;\n  overflow: hidden;\n  height: 200px;\n  position: relative;\n  border-color: transparent;\n  margin-bottom: 0;\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n\n  flex: 1;\n  flex-shrink: 0;\n  overflow: hidden;\n  height: 200px;\n  position: relative;\n  border-color: transparent;\n  margin-bottom: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=styles.jsx.map