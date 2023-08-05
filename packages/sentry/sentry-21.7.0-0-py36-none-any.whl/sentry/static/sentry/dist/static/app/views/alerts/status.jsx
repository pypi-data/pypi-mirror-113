Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("./types");
var Status = function (_a) {
    var className = _a.className, incident = _a.incident, disableIconColor = _a.disableIconColor;
    var status = incident.status;
    var isResolved = status === types_1.IncidentStatus.CLOSED;
    var isWarning = status === types_1.IncidentStatus.WARNING;
    var icon = isResolved ? (<icons_1.IconCheckmark color={disableIconColor ? undefined : 'green300'}/>) : isWarning ? (<icons_1.IconWarning color={disableIconColor ? undefined : 'orange400'}/>) : (<icons_1.IconFire color={disableIconColor ? undefined : 'red300'}/>);
    var text = isResolved ? locale_1.t('Resolved') : isWarning ? locale_1.t('Warning') : locale_1.t('Critical');
    return (<Wrapper className={className}>
      <Icon>{icon}</Icon>
      {text}
    </Wrapper>);
};
exports.default = Status;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n"])), space_1.default(0.75));
var Icon = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: -3px;\n"], ["\n  margin-bottom: -3px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=status.jsx.map