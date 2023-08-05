Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
/**
 * Renders an Alert box of type "error". Renders a "Retry" button only if a `onRetry` callback is defined.
 */
var LoadingError = /** @class */ (function (_super) {
    tslib_1.__extends(LoadingError, _super);
    function LoadingError() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LoadingError.prototype.shouldComponentUpdate = function () {
        return false;
    };
    LoadingError.prototype.render = function () {
        var _a = this.props, message = _a.message, onRetry = _a.onRetry;
        return (<StyledAlert type="error">
        <Content>
          <icons_1.IconInfo size="lg"/>
          <div data-test-id="loading-error-message">{message}</div>
          {onRetry && (<button_1.default onClick={onRetry} type="button" priority="default" size="small">
              {locale_1.t('Retry')}
            </button_1.default>)}
        </Content>
      </StyledAlert>);
    };
    LoadingError.defaultProps = {
        message: locale_1.t('There was an error loading data.'),
    };
    return LoadingError;
}(React.Component));
exports.default = LoadingError;
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", " & {\n    border-radius: 0;\n    border-width: 1px 0;\n  }\n"], ["\n  " /* sc-selector */, " & {\n    border-radius: 0;\n    border-width: 1px 0;\n  }\n"])), /* sc-selector */ panels_1.Panel);
var Content = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content auto max-content;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content auto max-content;\n  align-items: center;\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=loadingError.jsx.map