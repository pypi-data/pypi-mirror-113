Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var emailField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/emailField"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var OrganizationJoinRequest = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationJoinRequest, _super);
    function OrganizationJoinRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            submitSuccess: null,
        };
        _this.handleSubmitSuccess = function () {
            _this.setState({ submitSuccess: true });
        };
        _this.handleCancel = function (e) {
            e.preventDefault();
            var orgId = _this.props.params.orgId;
            window.location.assign("/auth/login/" + orgId + "/");
        };
        return _this;
    }
    OrganizationJoinRequest.prototype.componentDidMount = function () {
        var orgId = this.props.params.orgId;
        analytics_1.trackAdhocEvent({
            eventKey: 'join_request.viewed',
            org_slug: orgId,
        });
    };
    OrganizationJoinRequest.prototype.handleSubmitError = function () {
        indicator_1.addErrorMessage(locale_1.t('Request to join failed'));
    };
    OrganizationJoinRequest.prototype.render = function () {
        var orgId = this.props.params.orgId;
        var submitSuccess = this.state.submitSuccess;
        if (submitSuccess) {
            return (<narrowLayout_1.default maxWidth="550px">
          <SuccessModal>
            <StyledIconMegaphone size="5em"/>
            <StyledHeader>{locale_1.t('Request Sent')}</StyledHeader>
            <StyledText>{locale_1.t('Your request to join has been sent.')}</StyledText>
            <ReceiveEmailMessage>
              {locale_1.tct('You will receive an email when your request is approved.', { orgId: orgId })}
            </ReceiveEmailMessage>
          </SuccessModal>
        </narrowLayout_1.default>);
        }
        return (<narrowLayout_1.default maxWidth="650px">
        <StyledIconMegaphone size="5em"/>
        <StyledHeader>{locale_1.t('Request to Join')}</StyledHeader>
        <StyledText>
          {locale_1.tct('Ask the admins if you can join the [orgId] organization.', {
                orgId: orgId,
            })}
        </StyledText>
        <form_1.default requireChanges apiEndpoint={"/organizations/" + orgId + "/join-request/"} apiMethod="POST" submitLabel={locale_1.t('Request to Join')} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onCancel={this.handleCancel}>
          <StyledEmailField name="email" inline={false} label={locale_1.t('Email Address')} placeholder="name@example.com"/>
        </form_1.default>
      </narrowLayout_1.default>);
    };
    return OrganizationJoinRequest;
}(react_1.Component));
var SuccessModal = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  justify-items: center;\n  text-align: center;\n  padding-top: 10px;\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  justify-items: center;\n  text-align: center;\n  padding-top: 10px;\n  padding-bottom: ", ";\n"])), space_1.default(4));
var StyledIconMegaphone = styled_1.default(icons_1.IconMegaphone)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space_1.default(3));
var StyledHeader = styled_1.default('h3')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
var StyledText = styled_1.default('p')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var ReceiveEmailMessage = styled_1.default(StyledText)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  max-width: 250px;\n"], ["\n  max-width: 250px;\n"])));
var StyledEmailField = styled_1.default(emailField_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n  padding-left: 0;\n"], ["\n  padding-top: ", ";\n  padding-left: 0;\n"])), space_1.default(2));
exports.default = OrganizationJoinRequest;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=organizationJoinRequest.jsx.map