Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var author_1 = tslib_1.__importDefault(require("app/components/activity/author"));
var item_1 = tslib_1.__importDefault(require("app/components/activity/item"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var EventUserFeedback = /** @class */ (function (_super) {
    tslib_1.__extends(EventUserFeedback, _super);
    function EventUserFeedback() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventUserFeedback.prototype.getUrl = function () {
        var _a = this.props, report = _a.report, orgId = _a.orgId, issueId = _a.issueId;
        return "/organizations/" + orgId + "/issues/" + issueId + "/events/" + report.eventID + "/";
    };
    EventUserFeedback.prototype.render = function () {
        var _a = this.props, className = _a.className, report = _a.report;
        var user = report.user || {
            name: report.name,
            email: report.email,
            id: '',
            username: '',
            ip_address: '',
        };
        return (<div className={className}>
        <item_1.default date={report.dateCreated} author={{ type: 'user', user: user }} header={<div>
              <author_1.default>{report.name}</author_1.default>
              <clipboard_1.default value={report.email}>
                <Email>
                  {report.email}
                  <StyledIconCopy size="xs"/>
                </Email>
              </clipboard_1.default>
              {report.eventID && (<ViewEventLink to={this.getUrl()}>{locale_1.t('View event')}</ViewEventLink>)}
            </div>}>
          <p dangerouslySetInnerHTML={{
                __html: utils_1.nl2br(utils_1.escape(report.comments)),
            }}/>
        </item_1.default>
      </div>);
    };
    return EventUserFeedback;
}(react_1.Component));
exports.default = EventUserFeedback;
var Email = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  cursor: pointer;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  cursor: pointer;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(1));
var ViewEventLink = styled_1.default(link_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: 300;\n  margin-left: ", ";\n  font-size: 0.9em;\n"], ["\n  font-weight: 300;\n  margin-left: ", ";\n  font-size: 0.9em;\n"])), space_1.default(1));
var StyledIconCopy = styled_1.default(icons_1.IconCopy)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=userFeedback.jsx.map