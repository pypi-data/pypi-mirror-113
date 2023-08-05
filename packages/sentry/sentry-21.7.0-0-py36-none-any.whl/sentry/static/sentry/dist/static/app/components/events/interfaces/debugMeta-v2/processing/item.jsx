Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function Item(_a) {
    var type = _a.type, icon = _a.icon, className = _a.className;
    function getLabel() {
        switch (type) {
            case 'stack_unwinding':
                return locale_1.t('Stack Unwinding');
            case 'symbolication':
                return locale_1.t('Symbolication');
            default: {
                Sentry.captureException(new Error('Unknown Images Loaded processing item type'));
                return null; // This shall not happen
            }
        }
    }
    return (<Wrapper className={className}>
      {icon}
      {getLabel()}
    </Wrapper>);
}
exports.default = Item;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  white-space: nowrap;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  white-space: nowrap;\n"])), space_1.default(0.5), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=item.jsx.map