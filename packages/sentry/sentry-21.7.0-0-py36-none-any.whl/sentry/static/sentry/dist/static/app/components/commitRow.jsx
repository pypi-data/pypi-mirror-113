Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var commitLink_1 = tslib_1.__importDefault(require("app/components/commitLink"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var CommitRow = /** @class */ (function (_super) {
    tslib_1.__extends(CommitRow, _super);
    function CommitRow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CommitRow.prototype.renderMessage = function (message) {
        if (!message) {
            return locale_1.t('No message provided');
        }
        var firstLine = message.split(/\n/)[0];
        return firstLine;
    };
    CommitRow.prototype.renderHovercardBody = function (author) {
        return (<EmailWarning>
        {locale_1.tct('The email [actorEmail] is not a member of your organization. [inviteUser:Invite] them or link additional emails in [accountSettings:account settings].', {
                actorEmail: <strong>{author.email}</strong>,
                accountSettings: <StyledLink to="/settings/account/emails/"/>,
                inviteUser: (<StyledLink to="" onClick={function () {
                        return modal_1.openInviteMembersModal({
                            initialData: [
                                {
                                    emails: new Set([author.email]),
                                },
                            ],
                            source: 'suspect_commit',
                        });
                    }}/>),
            })}
      </EmailWarning>);
    };
    CommitRow.prototype.render = function () {
        var _a = this.props, commit = _a.commit, customAvatar = _a.customAvatar, props = tslib_1.__rest(_a, ["commit", "customAvatar"]);
        var id = commit.id, dateCreated = commit.dateCreated, message = commit.message, author = commit.author, repository = commit.repository;
        var nonMemberEmail = author && author.id === undefined;
        return (<panels_1.PanelItem key={id} {...props}>
        {customAvatar ? (customAvatar) : nonMemberEmail ? (<AvatarWrapper>
            <hovercard_1.default body={this.renderHovercardBody(author)}>
              <userAvatar_1.default size={36} user={author}/>
              <EmailWarningIcon>
                <icons_1.IconWarning size="xs"/>
              </EmailWarningIcon>
            </hovercard_1.default>
          </AvatarWrapper>) : (<AvatarWrapper>
            <userAvatar_1.default size={36} user={author}/>
          </AvatarWrapper>)}

        <CommitMessage>
          <Message>{this.renderMessage(message)}</Message>
          <Meta>
            {locale_1.tct('[author] committed [timeago]', {
                author: <strong>{(author && author.name) || locale_1.t('Unknown author')}</strong>,
                timeago: <timeSince_1.default date={dateCreated}/>,
            })}
          </Meta>
        </CommitMessage>

        <div>
          <commitLink_1.default commitId={id} repository={repository}/>
        </div>
      </panels_1.PanelItem>);
    };
    return CommitRow;
}(React.Component));
var AvatarWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  align-self: flex-start;\n  margin-right: ", ";\n"], ["\n  position: relative;\n  align-self: flex-start;\n  margin-right: ", ";\n"])), space_1.default(2));
var EmailWarning = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.4;\n  margin: -4px;\n"], ["\n  font-size: ", ";\n  line-height: 1.4;\n  margin: -4px;\n"])), function (p) { return p.theme.fontSizeSmall; });
var StyledLink = styled_1.default(link_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  border-bottom: 1px dotted ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  border-bottom: 1px dotted ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var EmailWarningIcon = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  bottom: -6px;\n  right: -7px;\n  line-height: 12px;\n  border-radius: 50%;\n  border: 1px solid ", ";\n  background: ", ";\n  padding: 1px 2px 3px 2px;\n"], ["\n  position: absolute;\n  bottom: -6px;\n  right: -7px;\n  line-height: 12px;\n  border-radius: 50%;\n  border: 1px solid ", ";\n  background: ", ";\n  padding: 1px 2px 3px 2px;\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.yellow200; });
var CommitMessage = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  flex-direction: column;\n  min-width: 0;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  flex-direction: column;\n  min-width: 0;\n  margin-right: ", ";\n"])), space_1.default(2));
var Message = styled_1.default(textOverflow_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: 15px;\n  line-height: 1.1;\n  font-weight: bold;\n"], ["\n  font-size: 15px;\n  line-height: 1.1;\n  font-weight: bold;\n"])));
var Meta = styled_1.default(textOverflow_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: 13px;\n  line-height: 1.5;\n  margin: 0;\n  color: ", ";\n"], ["\n  font-size: 13px;\n  line-height: 1.5;\n  margin: 0;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
exports.default = styled_1.default(CommitRow)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n"], ["\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=commitRow.jsx.map