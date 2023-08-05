Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var modal_1 = require("app/actionCreators/modal");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var SuggestedOwnerHovercard = /** @class */ (function (_super) {
    tslib_1.__extends(SuggestedOwnerHovercard, _super);
    function SuggestedOwnerHovercard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            commitsExpanded: false,
            rulesExpanded: false,
        };
        return _this;
    }
    SuggestedOwnerHovercard.prototype.render = function () {
        var _this = this;
        var _a = this.props, actor = _a.actor, commits = _a.commits, rules = _a.rules, props = tslib_1.__rest(_a, ["actor", "commits", "rules"]);
        var _b = this.state, commitsExpanded = _b.commitsExpanded, rulesExpanded = _b.rulesExpanded;
        return (<hovercard_1.default header={<React.Fragment>
            <HovercardHeader>
              <HovercardActorAvatar actor={actor}/>
              {actor.name || actor.email}
            </HovercardHeader>
            {actor.id === undefined && (<EmailAlert icon={<icons_1.IconWarning size="xs"/>} type="warning">
                {locale_1.tct('The email [actorEmail] is not a member of your organization. [inviteUser:Invite] them or link additional emails in [accountSettings:account settings].', {
                        actorEmail: <strong>{actor.email}</strong>,
                        accountSettings: <link_1.default to="/settings/account/emails/"/>,
                        inviteUser: (<a onClick={function () {
                                return modal_1.openInviteMembersModal({
                                    initialData: [
                                        {
                                            emails: new Set([actor.email]),
                                        },
                                    ],
                                    source: 'suggested_assignees',
                                });
                            }}/>),
                    })}
              </EmailAlert>)}
          </React.Fragment>} body={<HovercardBody>
            {commits !== undefined && (<React.Fragment>
                <div className="divider">
                  <h6>{locale_1.t('Commits')}</h6>
                </div>
                <div>
                  {commits
                        .slice(0, commitsExpanded ? commits.length : 3)
                        .map(function (_a, i) {
                        var message = _a.message, dateCreated = _a.dateCreated;
                        return (<CommitReasonItem key={i}>
                        <CommitIcon />
                        <CommitMessage message={message !== null && message !== void 0 ? message : undefined} date={dateCreated}/>
                      </CommitReasonItem>);
                    })}
                </div>
                {commits.length > 3 && !commitsExpanded ? (<ViewMoreButton onClick={function () { return _this.setState({ commitsExpanded: true }); }}/>) : null}
              </React.Fragment>)}
            {utils_1.defined(rules) && (<React.Fragment>
                <div className="divider">
                  <h6>{locale_1.t('Matching Ownership Rules')}</h6>
                </div>
                <div>
                  {rules
                        .slice(0, rulesExpanded ? rules.length : 3)
                        .map(function (_a, i) {
                        var _b = tslib_1.__read(_a, 2), type = _b[0], matched = _b[1];
                        return (<RuleReasonItem key={i}>
                        <OwnershipTag tagType={type}/>
                        <OwnershipValue>{matched}</OwnershipValue>
                      </RuleReasonItem>);
                    })}
                </div>
                {rules.length > 3 && !rulesExpanded ? (<ViewMoreButton onClick={function () { return _this.setState({ rulesExpanded: true }); }}/>) : null}
              </React.Fragment>)}
          </HovercardBody>} {...props}/>);
    };
    return SuggestedOwnerHovercard;
}(React.Component));
var tagColors = {
    url: theme_1.default.green200,
    path: theme_1.default.purple300,
    tag: theme_1.default.blue300,
};
var CommitIcon = styled_1.default(icons_1.IconCommit)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  flex-shrink: 0;\n"], ["\n  margin-right: ", ";\n  flex-shrink: 0;\n"])), space_1.default(0.5));
var CommitMessage = styled_1.default(function (_a) {
    var _b = _a.message, message = _b === void 0 ? '' : _b, date = _a.date, props = tslib_1.__rest(_a, ["message", "date"]);
    return (<div {...props}>
    {message.split('\n')[0]}
    <CommitDate date={date}/>
  </div>);
})(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-top: ", ";\n  hyphens: auto;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-top: ", ";\n  hyphens: auto;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(0.25));
var CommitDate = styled_1.default(function (_a) {
    var date = _a.date, props = tslib_1.__rest(_a, ["date"]);
    return (<div {...props}>{moment_1.default(date).fromNow()}</div>);
})(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  margin-top: ", ";\n  color: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.gray300; });
var CommitReasonItem = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(1));
var RuleReasonItem = styled_1.default('code')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(1));
var OwnershipTag = styled_1.default(function (_a) {
    var tagType = _a.tagType, props = tslib_1.__rest(_a, ["tagType"]);
    return <div {...props}>{tagType}</div>;
})(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  border-radius: 2px;\n  font-weight: bold;\n  min-width: 34px;\n  text-align: center;\n"], ["\n  background: ", ";\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  border-radius: 2px;\n  font-weight: bold;\n  min-width: 34px;\n  text-align: center;\n"])), function (p) { return tagColors[p.tagType.indexOf('tags') === -1 ? p.tagType : 'tag']; }, function (p) { return p.theme.white; }, function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(0.25), space_1.default(0.5), space_1.default(0.25), space_1.default(0.5), space_1.default(0.25));
var ViewMoreButton = styled_1.default(function (p) { return (<button_1.default {...p} priority="link" size="zero">
    {locale_1.t('View more')}
  </button_1.default>); })(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  border: none;\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  width: 100%;\n  min-width: 34px;\n"], ["\n  border: none;\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  width: 100%;\n  min-width: 34px;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(0.25), space_1.default(0.5), space_1.default(1), space_1.default(0.25), space_1.default(0.25));
var OwnershipValue = styled_1.default('code')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  word-break: break-all;\n  line-height: 1.2;\n"], ["\n  word-break: break-all;\n  line-height: 1.2;\n"])));
var EmailAlert = styled_1.default(alert_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin: 10px -13px -13px;\n  border-radius: 0;\n  border-color: #ece0b0;\n  padding: 10px;\n  font-size: ", ";\n  font-weight: normal;\n  box-shadow: none;\n"], ["\n  margin: 10px -13px -13px;\n  border-radius: 0;\n  border-color: #ece0b0;\n  padding: 10px;\n  font-size: ", ";\n  font-weight: normal;\n  box-shadow: none;\n"])), function (p) { return p.theme.fontSizeSmall; });
var HovercardHeader = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var HovercardActorAvatar = styled_1.default(function (p) { return (<actorAvatar_1.default size={20} hasTooltip={false} {...p}/>); })(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var HovercardBody = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  margin-top: -", ";\n"], ["\n  margin-top: -", ";\n"])), space_1.default(2));
exports.default = SuggestedOwnerHovercard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=suggestedOwnerHovercard.jsx.map