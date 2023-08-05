Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var integrationUtil_1 = require("app/utils/integrationUtil");
var textareaField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textareaField"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
/**
 * This modal serves as a non-owner's confirmation step before sending
 * organization owners an email requesting a new organization integration. It
 * lets the user attach an optional message to be included in the email.
 */
var RequestIntegrationModal = /** @class */ (function (_super) {
    tslib_1.__extends(RequestIntegrationModal, _super);
    function RequestIntegrationModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = tslib_1.__assign(tslib_1.__assign({}, _this.getDefaultState()), { isSending: false, message: '' });
        _this.sendRequest = function () {
            var _a = _this.props, organization = _a.organization, slug = _a.slug, type = _a.type;
            var message = _this.state.message;
            integrationUtil_1.trackIntegrationEvent('integrations.request_install', {
                integration_type: type,
                integration: slug,
            }, organization);
            var endpoint = "/organizations/" + organization.slug + "/integration-requests/";
            _this.api.request(endpoint, {
                method: 'POST',
                data: {
                    providerSlug: slug,
                    providerType: type,
                    message: message,
                },
                success: _this.handleSubmitSuccess,
                error: _this.handleSubmitError,
            });
        };
        _this.handleSubmitSuccess = function () {
            var _a = _this.props, closeModal = _a.closeModal, onSuccess = _a.onSuccess;
            indicator_1.addSuccessMessage(locale_1.t('Request successfully sent.'));
            _this.setState({ isSending: false });
            onSuccess();
            closeModal();
        };
        _this.handleSubmitError = function () {
            indicator_1.addErrorMessage('Error sending the request');
            _this.setState({ isSending: false });
        };
        return _this;
    }
    RequestIntegrationModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, name = _a.name;
        var buttonText = this.state.isSending ? locale_1.t('Sending Request') : locale_1.t('Send Request');
        return (<react_1.Fragment>
        <Header>
          <h4>{locale_1.t('Request %s Installation', name)}</h4>
        </Header>
        <Body>
          <textBlock_1.default>
            {locale_1.t('Looks like your organization owner, manager, or admin needs to install %s. Want to send them a request?', name)}
          </textBlock_1.default>
          <textBlock_1.default>
            {locale_1.t('(Optional) You’ve got good reasons for installing the %s Integration. Share them with your organization owner.', name)}
          </textBlock_1.default>
          <textareaField_1.default inline={false} flexibleControlStateSize stacked name="message" type="string" onChange={function (value) { return _this.setState({ message: value }); }} placeholder={locale_1.t('Optional message…')}/>
          <textBlock_1.default>
            {locale_1.t('When you click “Send Request”, we’ll email your request to your organization’s owners. So just keep that in mind.')}
          </textBlock_1.default>
        </Body>
        <Footer>
          <button_1.default onClick={this.sendRequest}>{buttonText}</button_1.default>
        </Footer>
      </react_1.Fragment>);
    };
    return RequestIntegrationModal;
}(asyncComponent_1.default));
exports.default = RequestIntegrationModal;
//# sourceMappingURL=RequestIntegrationModal.jsx.map