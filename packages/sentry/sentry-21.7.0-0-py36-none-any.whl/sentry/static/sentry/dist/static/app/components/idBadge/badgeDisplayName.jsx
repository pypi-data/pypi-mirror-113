Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var BadgeDisplayName = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  padding: ", " 0;\n"], ["\n  ", ";\n  padding: ", " 0;\n"])), function (p) {
    return p.hideOverflow &&
        "\n      " + overflowEllipsis_1.default + ";\n      max-width: " + (typeof p.hideOverflow === 'string'
            ? p.hideOverflow
            : p.theme.settings.maxCrumbWidth) + "\n  ";
}, space_1.default(0.25));
exports.default = BadgeDisplayName;
var templateObject_1;
//# sourceMappingURL=badgeDisplayName.jsx.map