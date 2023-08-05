Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var groupBy_1 = tslib_1.__importDefault(require("lodash/groupBy"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var indicator_1 = require("app/actionCreators/indicator");
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var panels_1 = require("app/components/panels");
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var ENDPOINT = '/users/me/subscriptions/';
var AccountSubscriptions = /** @class */ (function (_super) {
    tslib_1.__extends(AccountSubscriptions, _super);
    function AccountSubscriptions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleToggle = function (subscription, index, _e) {
            var subscribed = !subscription.subscribed;
            var oldSubscriptions = _this.state.subscriptions;
            _this.setState(function (state) {
                var newSubscriptions = state.subscriptions.slice();
                newSubscriptions[index] = tslib_1.__assign(tslib_1.__assign({}, subscription), { subscribed: subscribed, subscribedDate: new Date().toString() });
                return tslib_1.__assign(tslib_1.__assign({}, state), { subscriptions: newSubscriptions });
            });
            _this.api.request(ENDPOINT, {
                method: 'PUT',
                data: {
                    listId: subscription.listId,
                    subscribed: subscribed,
                },
                success: function () {
                    indicator_1.addSuccessMessage((subscribed ? 'Subscribed' : 'Unsubscribed') + " to " + subscription.listName);
                },
                error: function () {
                    indicator_1.addErrorMessage("Unable to " + (subscribed ? '' : 'un') + "subscribe to " + subscription.listName);
                    _this.setState({ subscriptions: oldSubscriptions });
                },
            });
        };
        return _this;
    }
    AccountSubscriptions.prototype.getEndpoints = function () {
        return [['subscriptions', ENDPOINT]];
    };
    AccountSubscriptions.prototype.getTitle = function () {
        return 'Subscriptions';
    };
    AccountSubscriptions.prototype.renderBody = function () {
        var _this = this;
        var subGroups = Object.entries(groupBy_1.default(this.state.subscriptions, function (sub) { return sub.email; }));
        return (<div>
        <settingsPageHeader_1.default title="Subscriptions"/>
        <textBlock_1.default>
          {locale_1.t("Sentry is committed to respecting your inbox. Our goal is to\n              provide useful content and resources that make fixing errors less\n              painful. Enjoyable even.")}
        </textBlock_1.default>

        <textBlock_1.default>
          {locale_1.t("As part of our compliance with the EU\u2019s General Data Protection\n              Regulation (GDPR), starting on 25 May 2018, we\u2019ll only email you\n              according to the marketing categories to which you\u2019ve explicitly\n              opted-in.")}
        </textBlock_1.default>

        <panels_1.Panel>
          {this.state.subscriptions.length ? (<div>
              <panels_1.PanelHeader>{locale_1.t('Subscription')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                {subGroups.map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), email = _b[0], subscriptions = _b[1];
                    return (<React.Fragment key={email}>
                    {subGroups.length > 1 && (<Heading>
                        <icons_1.IconToggle /> {locale_1.t('Subscriptions for %s', email)}
                      </Heading>)}

                    {subscriptions.map(function (subscription, index) { return (<panels_1.PanelItem center key={subscription.listId}>
                        <SubscriptionDetails>
                          <SubscriptionName>{subscription.listName}</SubscriptionName>
                          {subscription.listDescription && (<Description>{subscription.listDescription}</Description>)}
                          {subscription.subscribed ? (<SubscribedDescription>
                              <div>
                                {locale_1.tct('[email] on [date]', {
                                    email: subscription.email,
                                    date: (<dateTime_1.default shortDate date={moment_1.default(subscription.subscribedDate)}/>),
                                })}
                              </div>
                            </SubscribedDescription>) : (<SubscribedDescription>
                              {locale_1.t('Not currently subscribed')}
                            </SubscribedDescription>)}
                        </SubscriptionDetails>
                        <div>
                          <switchButton_1.default isActive={subscription.subscribed} size="lg" toggle={_this.handleToggle.bind(_this, subscription, index)}/>
                        </div>
                      </panels_1.PanelItem>); })}
                  </React.Fragment>);
                })}
              </panels_1.PanelBody>
            </div>) : (<emptyMessage_1.default>{locale_1.t("There's no subscription backend present.")}</emptyMessage_1.default>)}
        </panels_1.Panel>
        <textBlock_1.default>
          {locale_1.t("We\u2019re applying GDPR consent and privacy policies to all Sentry\n              contacts, regardless of location. You\u2019ll be able to manage your\n              subscriptions here and from an Unsubscribe link in the footer of\n              all marketing emails.")}
        </textBlock_1.default>

        <textBlock_1.default>
          {locale_1.tct('Please contact [email:learn@sentry.io] with any questions or suggestions.', { email: <a href="mailto:learn@sentry.io"/> })}
        </textBlock_1.default>
      </div>);
    };
    return AccountSubscriptions;
}(asyncView_1.default));
var Heading = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  padding: ", " ", ";\n  background: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  padding: ", " ", ";\n  background: ", ";\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeMedium; }, space_1.default(1.5), space_1.default(2), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; });
var SubscriptionDetails = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 50%;\n  padding-right: ", ";\n"], ["\n  width: 50%;\n  padding-right: ", ";\n"])), space_1.default(2));
var SubscriptionName = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var Description = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.75), function (p) { return p.theme.subText; });
var SubscribedDescription = styled_1.default(Description)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
exports.default = AccountSubscriptions;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=accountSubscriptions.jsx.map