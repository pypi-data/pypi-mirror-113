Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var constants_1 = require("./constants");
var StatusWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var IntegrationStatus = styled_1.default(react_1.withTheme(function (props) {
    var theme = props.theme, status = props.status, p = tslib_1.__rest(props, ["theme", "status"]);
    return (<StatusWrapper>
        <circleIndicator_1.default size={6} color={theme[constants_1.COLORS[status]]}/>
        <div {...p}>{"" + locale_1.t(status)}</div>
      </StatusWrapper>);
}))(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n  font-weight: light;\n  margin-right: ", ";\n"], ["\n  color: ", ";\n  margin-left: ", ";\n  font-weight: light;\n  margin-right: ", ";\n"])), function (p) { return p.theme[constants_1.COLORS[p.status]]; }, space_1.default(0.5), space_1.default(0.75));
exports.default = IntegrationStatus;
var templateObject_1, templateObject_2;
//# sourceMappingURL=integrationStatus.jsx.map