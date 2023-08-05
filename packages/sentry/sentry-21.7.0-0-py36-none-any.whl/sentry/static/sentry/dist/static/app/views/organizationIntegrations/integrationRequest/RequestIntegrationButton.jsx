Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RequestIntegrationModal_1 = tslib_1.__importDefault(require("./RequestIntegrationModal"));
var RequestIntegrationButton = /** @class */ (function (_super) {
    tslib_1.__extends(RequestIntegrationButton, _super);
    function RequestIntegrationButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
            isSent: false,
        };
        return _this;
    }
    RequestIntegrationButton.prototype.openRequestModal = function () {
        var _this = this;
        this.setState({ isOpen: true });
        modal_1.openModal(function (renderProps) { return (<RequestIntegrationModal_1.default {..._this.props} {...renderProps} onSuccess={function () { return _this.setState({ isSent: true }); }}/>); }, {
            onClose: function () { return _this.setState({ isOpen: false }); },
        });
    };
    RequestIntegrationButton.prototype.render = function () {
        var _this = this;
        var _a = this.state, isOpen = _a.isOpen, isSent = _a.isSent;
        var buttonText;
        if (isOpen) {
            buttonText = locale_1.t('Requesting Installation');
        }
        else if (isSent) {
            buttonText = locale_1.t('Installation Requested');
        }
        else {
            buttonText = locale_1.t('Request Installation');
        }
        return (<StyledRequestIntegrationButton data-test-id="request-integration-button" disabled={isOpen || isSent} onClick={function () { return _this.openRequestModal(); }} priority="primary" size="small">
        {buttonText}
      </StyledRequestIntegrationButton>);
    };
    return RequestIntegrationButton;
}(react_1.Component));
exports.default = RequestIntegrationButton;
var StyledRequestIntegrationButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=RequestIntegrationButton.jsx.map