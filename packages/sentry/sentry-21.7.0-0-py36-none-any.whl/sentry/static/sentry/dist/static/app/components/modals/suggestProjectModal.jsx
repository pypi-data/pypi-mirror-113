Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var qs = tslib_1.__importStar(require("query-string"));
var mobile_hero_jpg_1 = tslib_1.__importDefault(require("sentry-images/spot/mobile-hero.jpg"));
var indicator_1 = require("app/actionCreators/indicator");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var emailField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/emailField"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var SuggestProjectModal = /** @class */ (function (_super) {
    tslib_1.__extends(SuggestProjectModal, _super);
    function SuggestProjectModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            askTeammate: false,
        };
        _this.handleGetStartedClick = function () {
            var _a = _this.props, matchedUserAgentString = _a.matchedUserAgentString, organization = _a.organization;
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.clicked_mobile_prompt_setup_project', { matchedUserAgentString: matchedUserAgentString }, organization);
        };
        _this.handleAskTeammate = function () {
            var _a = _this.props, matchedUserAgentString = _a.matchedUserAgentString, organization = _a.organization;
            _this.setState({ askTeammate: true });
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.clicked_mobile_prompt_ask_teammate', { matchedUserAgentString: matchedUserAgentString }, organization);
        };
        _this.goBack = function () {
            _this.setState({ askTeammate: false });
        };
        _this.handleSubmitSuccess = function () {
            var _a = _this.props, matchedUserAgentString = _a.matchedUserAgentString, organization = _a.organization, closeModal = _a.closeModal;
            indicator_1.addSuccessMessage('Notified teammate successfully');
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.submitted_mobile_prompt_ask_teammate', { matchedUserAgentString: matchedUserAgentString }, organization);
            closeModal();
        };
        _this.handlePreSubmit = function () {
            indicator_1.addLoadingMessage(locale_1.t('Submitting\u2026'));
        };
        _this.handleSubmitError = function () {
            indicator_1.addErrorMessage(locale_1.t('Error notifying teammate'));
        };
        return _this;
    }
    SuggestProjectModal.prototype.renderAskTeammate = function () {
        var _a = this.props, Body = _a.Body, organization = _a.organization;
        return (<Body>
        <form_1.default apiEndpoint={"/organizations/" + organization.slug + "/request-project-creation/"} apiMethod="POST" submitLabel={locale_1.t('Send')} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onPreSubmit={this.handlePreSubmit} extraButton={<BackWrapper>
              <StyledBackButton onClick={this.goBack}>{locale_1.t('Back')}</StyledBackButton>
            </BackWrapper>}>
          <p>
            {locale_1.t('Let the right folks know about Sentry Mobile Application Monitoring.')}
          </p>
          <emailField_1.default required name="targetUserEmail" inline={false} label={locale_1.t('Email Address')} placeholder="name@example.com" stacked/>
        </form_1.default>
      </Body>);
    };
    SuggestProjectModal.prototype.renderMain = function () {
        var _this = this;
        var _a = this.props, Body = _a.Body, Footer = _a.Footer, organization = _a.organization;
        var paramString = qs.stringify({
            referrer: 'suggest_project',
            category: 'mobile',
        });
        var newProjectLink = "/organizations/" + organization.slug + "/projects/new/?" + paramString;
        return (<react_1.Fragment>
        <Body>
          <ModalContainer>
            <SmallP>
              {locale_1.t("Sentry for Mobile shows a holistic overview of your application's health in real time. So you can correlate errors with releases, tags, and devices to solve problems quickly, decrease churn, and improve user retention.")}
            </SmallP>

            <StyledList symbol="bullet">
              <listItem_1.default>
                {locale_1.tct('[see:See] session data, version adoption, and user impact by every release.', {
                see: <strong />,
            })}
              </listItem_1.default>
              <listItem_1.default>
                {locale_1.tct('[solve:Solve] issues quickly with full context: contextualized stack traces, events that lead to the error, client, hardware information, and the very commit that introduced the error.', {
                solve: <strong />,
            })}
              </listItem_1.default>
              <listItem_1.default>
                {locale_1.tct('[learn:Learn] and analyze event data to reduce regressions and ultimately improve user adoption and engagement.', {
                learn: <strong />,
            })}
              </listItem_1.default>
            </StyledList>

            <SmallP>{locale_1.t('And guess what? Setup takes less than five minutes.')}</SmallP>
          </ModalContainer>
        </Body>
        <Footer>
          <access_1.default organization={organization} access={['project:write']}>
            {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<buttonBar_1.default gap={1}>
                <button_1.default priority={hasAccess ? 'default' : 'primary'} onClick={_this.handleAskTeammate}>
                  {locale_1.t('Tell a Teammate')}
                </button_1.default>
                {hasAccess && (<button_1.default href={newProjectLink} onClick={_this.handleGetStartedClick} priority="primary">
                    {locale_1.t('Get Started')}
                  </button_1.default>)}
              </buttonBar_1.default>);
            }}
          </access_1.default>
        </Footer>
      </react_1.Fragment>);
    };
    SuggestProjectModal.prototype.render = function () {
        var Header = this.props.Header;
        var askTeammate = this.state.askTeammate;
        var header = askTeammate ? locale_1.t('Tell a Teammate') : locale_1.t('Try Sentry for Mobile');
        return (<react_1.Fragment>
        <Header>
          <PatternHeader />
          <Title>{header}</Title>
        </Header>
        {this.state.askTeammate ? this.renderAskTeammate() : this.renderMain()}
      </react_1.Fragment>);
    };
    return SuggestProjectModal;
}(react_1.Component));
var ModalContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"])), space_1.default(3));
var Title = styled_1.default('h3')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(2), space_1.default(3));
var SmallP = styled_1.default('p')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var PatternHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: -", " -", " 0 -", ";\n  border-radius: 7px 7px 0 0;\n  background-image: url(", ");\n  background-size: 475px;\n  background-color: black;\n  background-repeat: no-repeat;\n  overflow: hidden;\n  background-position: center bottom;\n  height: 156px;\n"], ["\n  margin: -", " -", " 0 -", ";\n  border-radius: 7px 7px 0 0;\n  background-image: url(", ");\n  background-size: 475px;\n  background-color: black;\n  background-repeat: no-repeat;\n  overflow: hidden;\n  background-position: center bottom;\n  height: 156px;\n"])), space_1.default(4), space_1.default(4), space_1.default(4), mobile_hero_jpg_1.default);
var StyledList = styled_1.default(list_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  li {\n    padding-left: ", ";\n  }\n"], ["\n  li {\n    padding-left: ", ";\n  }\n"])), space_1.default(3));
var BackWrapper = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  margin-right: ", ";\n"], ["\n  width: 100%;\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledBackButton = styled_1.default(button_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  float: right;\n"], ["\n  float: right;\n"])));
exports.default = withApi_1.default(SuggestProjectModal);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=suggestProjectModal.jsx.map