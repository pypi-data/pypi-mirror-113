Object.defineProperty(exports, "__esModule", { value: true });
exports.CauseHeader = exports.BannerSummary = exports.BannerContainer = exports.DataSection = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.DataSection = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  padding: ", " 0;\n  border-top: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", " 0 40px;\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  padding: ", " 0;\n  border-top: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", " 0 40px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(3), space_1.default(4));
function getColors(_a) {
    var priority = _a.priority, theme = _a.theme;
    var COLORS = {
        default: {
            background: theme.backgroundSecondary,
            border: theme.border,
        },
        danger: {
            background: theme.alert.error.backgroundLight,
            border: theme.alert.error.border,
        },
        success: {
            background: theme.alert.success.backgroundLight,
            border: theme.alert.success.border,
        },
    };
    return COLORS[priority];
}
exports.BannerContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n\n  background: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n\n  /* Muted box & processing errors are in different parts of the DOM */\n  &\n    + ", ":first-child,\n    &\n    + div\n    > ", ":first-child {\n    border-top: 0;\n  }\n"], ["\n  font-size: ", ";\n\n  background: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n\n  /* Muted box & processing errors are in different parts of the DOM */\n  &\n    + " /* sc-selector */, ":first-child,\n    &\n    + div\n    > " /* sc-selector */, ":first-child {\n    border-top: 0;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return getColors(p).background; }, function (p) { return getColors(p).border; }, function (p) { return getColors(p).border; }, /* sc-selector */ exports.DataSection, /* sc-selector */ exports.DataSection);
exports.BannerSummary = styled_1.default('p')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  padding: ", " ", " ", " 40px;\n  margin-bottom: 0;\n\n  /* Get icons in top right of content box */\n  & > .icon,\n  & > svg {\n    flex-shrink: 0;\n    flex-grow: 0;\n    margin-right: ", ";\n    margin-top: 2px;\n  }\n\n  & > span {\n    flex-grow: 1;\n  }\n\n  & > a {\n    align-self: flex-end;\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  padding: ", " ", " ", " 40px;\n  margin-bottom: 0;\n\n  /* Get icons in top right of content box */\n  & > .icon,\n  & > svg {\n    flex-shrink: 0;\n    flex-grow: 0;\n    margin-right: ", ";\n    margin-top: 2px;\n  }\n\n  & > span {\n    flex-grow: 1;\n  }\n\n  & > a {\n    align-self: flex-end;\n  }\n"])), space_1.default(2), space_1.default(4), space_1.default(2), space_1.default(1));
exports.CauseHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin-bottom: ", ";\n\n  & button,\n  & h3 {\n    color: ", ";\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    text-transform: uppercase;\n  }\n\n  & h3 {\n    margin-bottom: 0;\n  }\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin-bottom: ", ";\n\n  & button,\n  & h3 {\n    color: ", ";\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    text-transform: uppercase;\n  }\n\n  & h3 {\n    margin-bottom: 0;\n  }\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n  }\n"])), space_1.default(3), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=styles.jsx.map