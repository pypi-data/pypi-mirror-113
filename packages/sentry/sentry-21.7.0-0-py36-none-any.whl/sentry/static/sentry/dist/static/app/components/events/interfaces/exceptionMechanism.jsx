Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var forOwn_1 = tslib_1.__importDefault(require("lodash/forOwn"));
var isNil_1 = tslib_1.__importDefault(require("lodash/isNil"));
var isObject_1 = tslib_1.__importDefault(require("lodash/isObject"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pill_1 = tslib_1.__importDefault(require("app/components/pill"));
var pills_1 = tslib_1.__importDefault(require("app/components/pills"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var ExceptionMechanism = /** @class */ (function (_super) {
    tslib_1.__extends(ExceptionMechanism, _super);
    function ExceptionMechanism() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ExceptionMechanism.prototype.render = function () {
        var mechanism = this.props.data;
        var type = mechanism.type, description = mechanism.description, help_link = mechanism.help_link, handled = mechanism.handled, _a = mechanism.meta, meta = _a === void 0 ? {} : _a, _b = mechanism.data, data = _b === void 0 ? {} : _b;
        var errno = meta.errno, signal = meta.signal, mach_exception = meta.mach_exception;
        var linkElement = help_link && utils_1.isUrl(help_link) && (<StyledExternalLink href={help_link}>
        <icons_1.IconOpen size="xs"/>
      </StyledExternalLink>);
        var descriptionElement = description && (<hovercard_1.default header={<span>
            <Details>{locale_1.t('Details')}</Details> {linkElement}
          </span>} body={description}>
        <StyledIconInfo size="14px"/>
      </hovercard_1.default>);
        var pills = [
            <pill_1.default key="mechanism" name="mechanism" value={type || 'unknown'}>
        {descriptionElement || linkElement}
      </pill_1.default>,
        ];
        if (!isNil_1.default(handled)) {
            pills.push(<pill_1.default key="handled" name="handled" value={handled}/>);
        }
        if (errno) {
            var value = errno.name || errno.number;
            pills.push(<pill_1.default key="errno" name="errno" value={value}/>);
        }
        if (mach_exception) {
            var value = mach_exception.name || mach_exception.exception;
            pills.push(<pill_1.default key="mach" name="mach exception" value={value}/>);
        }
        if (signal) {
            var code = signal.code_name || locale_1.t('code') + " " + signal.code;
            var name_1 = signal.name || signal.number;
            var value = isNil_1.default(signal.code) ? name_1 : name_1 + " (" + code + ")";
            pills.push(<pill_1.default key="signal" name="signal" value={value}/>);
        }
        forOwn_1.default(data, function (value, key) {
            if (!isObject_1.default(value)) {
                pills.push(<pill_1.default key={"data:" + key} name={key} value={value}/>);
            }
        });
        return (<Wrapper>
        <pills_1.default>{pills}</pills_1.default>
      </Wrapper>);
    };
    return ExceptionMechanism;
}(react_1.Component));
exports.default = ExceptionMechanism;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space_1.default(2));
var iconStyle = function (p) { return react_2.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  transition: 0.1s linear color;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  transition: 0.1s linear color;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), p.theme.gray300, p.theme.gray500); };
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-flex !important;\n  ", ";\n"], ["\n  display: inline-flex !important;\n  ", ";\n"])), iconStyle);
var Details = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledIconInfo = styled_1.default(icons_1.IconInfo)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  ", ";\n"], ["\n  display: flex;\n  ", ";\n"])), iconStyle);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=exceptionMechanism.jsx.map