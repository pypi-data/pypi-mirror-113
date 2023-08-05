Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var styles_1 = require("app/components/charts/styles");
var times_1 = tslib_1.__importDefault(require("app/components/group/times"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var seenByList_1 = tslib_1.__importDefault(require("app/components/seenByList"));
var shortId_1 = tslib_1.__importDefault(require("app/components/shortId"));
var groupChart_1 = tslib_1.__importDefault(require("app/components/stream/groupChart"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var LinkedIssue = /** @class */ (function (_super) {
    tslib_1.__extends(LinkedIssue, _super);
    function LinkedIssue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LinkedIssue.prototype.getEndpoints = function () {
        var groupId = this.props.groupId;
        var groupUrl = "/issues/" + groupId + "/";
        return [['group', groupUrl]];
    };
    LinkedIssue.prototype.renderLoading = function () {
        return <placeholder_1.default height="120px" bottomGutter={2}/>;
    };
    LinkedIssue.prototype.renderError = function (error, disableLog, disableReport) {
        if (disableLog === void 0) { disableLog = false; }
        if (disableReport === void 0) { disableReport = false; }
        var errors = this.state.errors;
        var hasNotFound = Object.values(errors).find(function (resp) { return resp && resp.status === 404; });
        if (hasNotFound) {
            return (<alert_1.default type="warning" icon={<icons_1.IconWarning size="md"/>}>
          {locale_1.t('The linked issue cannot be found. It may have been deleted, or merged.')}
        </alert_1.default>);
        }
        return _super.prototype.renderError.call(this, error, disableLog, disableReport);
    };
    LinkedIssue.prototype.renderBody = function () {
        var eventId = this.props.eventId;
        var group = this.state.group;
        var issueUrl = group.permalink + "events/" + eventId + "/";
        return (<Section>
        <styles_1.SectionHeading>{locale_1.t('Event Issue')}</styles_1.SectionHeading>
        <StyledIssueCard>
          <IssueCardHeader>
            <StyledLink to={issueUrl} data-test-id="linked-issue">
              <StyledShortId shortId={group.shortId} avatar={<projectBadge_1.default project={group.project} avatarSize={16} hideName disableLink/>}/>
            </StyledLink>
            <StyledSeenByList seenBy={group.seenBy} maxVisibleAvatars={5}/>
          </IssueCardHeader>
          <IssueCardBody>
            <groupChart_1.default statsPeriod="30d" data={group} height={56}/>
          </IssueCardBody>
          <IssueCardFooter>
            <times_1.default lastSeen={group.lastSeen} firstSeen={group.firstSeen}/>
          </IssueCardFooter>
        </StyledIssueCard>
      </Section>);
    };
    return LinkedIssue;
}(asyncComponent_1.default));
var Section = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(4));
var StyledIssueCard = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border: 1px solid ", ";\n  border-radius: ", ";\n"], ["\n  border: 1px solid ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
var IssueCardHeader = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"])), space_1.default(1));
var StyledLink = styled_1.default(link_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-start;\n"], ["\n  justify-content: flex-start;\n"])));
var IssueCardBody = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  padding-top: ", ";\n"], ["\n  background: ", ";\n  padding-top: ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, space_1.default(1));
var StyledSeenByList = styled_1.default(seenByList_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var StyledShortId = styled_1.default(shortId_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.textColor; });
var IssueCardFooter = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.5), space_1.default(1));
exports.default = LinkedIssue;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=linkedIssue.jsx.map