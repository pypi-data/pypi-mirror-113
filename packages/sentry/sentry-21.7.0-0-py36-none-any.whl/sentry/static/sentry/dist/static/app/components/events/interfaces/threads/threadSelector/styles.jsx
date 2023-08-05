Object.defineProperty(exports, "__esModule", { value: true });
exports.GridCell = exports.Grid = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Grid = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-template-columns: 30px 2.5fr 4fr 0fr 40px;\n  @media (min-width: ", ") {\n    grid-template-columns: 40px 2.5fr 3.5fr 105px 40px;\n  }\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-template-columns: 30px 2.5fr 4fr 0fr 40px;\n  @media (min-width: ", ") {\n    grid-template-columns: 40px 2.5fr 3.5fr 105px 40px;\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(1), function (p) { return p.theme.breakpoints[0]; });
exports.Grid = Grid;
var GridCell = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
exports.GridCell = GridCell;
var templateObject_1, templateObject_2;
//# sourceMappingURL=styles.jsx.map