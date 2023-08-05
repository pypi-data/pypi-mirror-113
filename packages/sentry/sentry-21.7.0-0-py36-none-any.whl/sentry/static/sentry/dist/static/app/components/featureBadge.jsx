Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var tagDeprecated_1 = tslib_1.__importDefault(require("app/components/tagDeprecated"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var defaultTitles = {
    alpha: locale_1.t('This feature is internal and available for QA purposes'),
    beta: locale_1.t('This feature is available for early adopters and may change'),
    new: locale_1.t('This feature is new! Try it out and let us know what you think'),
};
var labels = {
    alpha: locale_1.t('alpha'),
    beta: locale_1.t('beta'),
    new: locale_1.t('new'),
};
var FeatureBadge = function (_a) {
    var type = _a.type, _b = _a.variant, variant = _b === void 0 ? 'badge' : _b, title = _a.title, theme = _a.theme, noTooltip = _a.noTooltip, p = tslib_1.__rest(_a, ["type", "variant", "title", "theme", "noTooltip"]);
    return (<div {...p}>
    <tooltip_1.default title={title !== null && title !== void 0 ? title : defaultTitles[type]} disabled={noTooltip} position="right">
      <React.Fragment>
        {variant === 'badge' && <StyledTag priority={type}>{labels[type]}</StyledTag>}
        {variant === 'indicator' && (<circleIndicator_1.default color={theme.badge[type].indicatorColor} size={8}/>)}
      </React.Fragment>
    </tooltip_1.default>
  </div>);
};
var StyledTag = styled_1.default(tagDeprecated_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 3px ", ";\n"], ["\n  padding: 3px ", ";\n"])), space_1.default(0.75));
var StyledFeatureBadge = styled_1.default(react_1.withTheme(FeatureBadge))(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n  margin-left: ", ";\n  position: relative;\n  top: -1px;\n"], ["\n  display: inline-flex;\n  align-items: center;\n  margin-left: ", ";\n  position: relative;\n  top: -1px;\n"])), space_1.default(0.75));
exports.default = StyledFeatureBadge;
var templateObject_1, templateObject_2;
//# sourceMappingURL=featureBadge.jsx.map