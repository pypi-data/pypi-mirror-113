Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var react_1 = require("@sentry/react");
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var userFeedback_1 = tslib_1.__importDefault(require("app/components/events/userFeedback"));
var compactIssue_1 = tslib_1.__importDefault(require("app/components/issues/compactIssue"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var userFeedbackEmpty_1 = tslib_1.__importDefault(require("./userFeedbackEmpty"));
var utils_1 = require("./utils");
var OrganizationUserFeedback = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationUserFeedback, _super);
    function OrganizationUserFeedback() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationUserFeedback.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, search = _a.location.search;
        return [
            [
                'reportList',
                "/organizations/" + organization.slug + "/user-feedback/",
                {
                    query: utils_1.getQuery(search),
                },
            ],
        ];
    };
    OrganizationUserFeedback.prototype.getTitle = function () {
        return locale_1.t('User Feedback') + " - " + this.props.organization.slug;
    };
    Object.defineProperty(OrganizationUserFeedback.prototype, "projectIds", {
        get: function () {
            var project = this.props.location.query.project;
            return Array.isArray(project)
                ? project
                : typeof project === 'string'
                    ? [project]
                    : [];
        },
        enumerable: false,
        configurable: true
    });
    OrganizationUserFeedback.prototype.renderResults = function () {
        var orgId = this.props.params.orgId;
        return (<panels_1.Panel className="issue-list" data-test-id="user-feedback-list">
        {this.state.reportList.map(function (item) {
                var issue = item.issue;
                return (<compactIssue_1.default key={item.id} id={issue.id} data={issue} eventId={item.eventID}>
              <StyledEventUserFeedback report={item} orgId={orgId} issueId={issue.id}/>
            </compactIssue_1.default>);
            })}
      </panels_1.Panel>);
    };
    OrganizationUserFeedback.prototype.renderEmpty = function () {
        return <userFeedbackEmpty_1.default projectIds={this.projectIds}/>;
    };
    OrganizationUserFeedback.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationUserFeedback.prototype.renderStreamBody = function () {
        var _a = this.state, loading = _a.loading, reportList = _a.reportList;
        if (loading) {
            return (<panels_1.Panel>
          <loadingIndicator_1.default />
        </panels_1.Panel>);
        }
        if (!reportList.length) {
            return this.renderEmpty();
        }
        return this.renderResults();
    };
    OrganizationUserFeedback.prototype.renderBody = function () {
        var organization = this.props.organization;
        var location = this.props.location;
        var pathname = location.pathname, search = location.search, query = location.query;
        var status = utils_1.getQuery(search).status;
        var reportListPageLinks = this.state.reportListPageLinks;
        var unresolvedQuery = omit_1.default(query, 'status');
        var allIssuesQuery = tslib_1.__assign(tslib_1.__assign({}, query), { status: '' });
        return (<globalSelectionHeader_1.default>
        <organization_1.PageContent>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            <div data-test-id="user-feedback">
              <Header>
                <pageHeading_1.default>{locale_1.t('User Feedback')}</pageHeading_1.default>
                <buttonBar_1.default active={!Array.isArray(status) ? status || '' : ''} merged>
                  <button_1.default size="small" barId="unresolved" to={{ pathname: pathname, query: unresolvedQuery }}>
                    {locale_1.t('Unresolved')}
                  </button_1.default>
                  <button_1.default size="small" barId="" to={{ pathname: pathname, query: allIssuesQuery }}>
                    {locale_1.t('All Issues')}
                  </button_1.default>
                </buttonBar_1.default>
              </Header>
              {this.renderStreamBody()}
              <pagination_1.default pageLinks={reportListPageLinks}/>
            </div>
          </lightWeightNoProjectMessage_1.default>
        </organization_1.PageContent>
      </globalSelectionHeader_1.default>);
    };
    return OrganizationUserFeedback;
}(asyncView_1.default));
exports.default = withOrganization_1.default(react_1.withProfiler(OrganizationUserFeedback));
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space_1.default(2));
var StyledEventUserFeedback = styled_1.default(userFeedback_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0 0;\n"], ["\n  margin: ", " 0 0;\n"])), space_1.default(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map