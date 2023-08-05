Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var styles_1 = require("app/components/charts/styles");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var groupList_1 = tslib_1.__importDefault(require("app/components/issues/groupList"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var constants_1 = require("app/views/alerts/incidentRules/constants");
var RelatedIssues = /** @class */ (function (_super) {
    tslib_1.__extends(RelatedIssues, _super);
    function RelatedIssues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderEmptyMessage = function () {
            return (<panels_1.Panel>
        <panels_1.PanelBody>
          <emptyStateWarning_1.default small withIcon={false}>
            {locale_1.t('No issues for this alert rule')}
          </emptyStateWarning_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
        };
        return _this;
    }
    RelatedIssues.prototype.render = function () {
        var _a;
        var _b = this.props, rule = _b.rule, projects = _b.projects, organization = _b.organization, timePeriod = _b.timePeriod;
        var start = timePeriod.start, end = timePeriod.end;
        var path = "/organizations/" + organization.slug + "/issues/";
        var queryParams = tslib_1.__assign(tslib_1.__assign({ start: start, end: end, groupStatsPeriod: 'auto', limit: 5 }, (rule.environment ? { environment: rule.environment } : {})), { sort: rule.aggregate === 'count_unique(user)' ? 'user' : 'freq', query: [
                rule.query,
                ((_a = rule.eventTypes) === null || _a === void 0 ? void 0 : _a.length)
                    ? "event.type:[" + rule.eventTypes.join(", ") + "]"
                    : constants_1.DATASET_EVENT_TYPE_FILTERS[rule.dataset],
            ].join(' '), project: projects.map(function (project) { return project.id; }) });
        var issueSearch = {
            pathname: "/organizations/" + organization.slug + "/issues/",
            query: queryParams,
        };
        return (<react_1.Fragment>
        <ControlsWrapper>
          <StyledSectionHeading>
            {locale_1.t('Related Issues')}
            <tooltip_1.default title={locale_1.t('Top issues containing events matching the metric.')}>
              <icons_1.IconInfo size="xs" color="gray200"/>
            </tooltip_1.default>
          </StyledSectionHeading>
          <button_1.default data-test-id="issues-open" size="small" to={issueSearch}>
            {locale_1.t('Open in Issues')}
          </button_1.default>
        </ControlsWrapper>

        <TableWrapper>
          <groupList_1.default orgId={organization.slug} endpointPath={path} queryParams={queryParams} query={"start=" + start + "&end=" + end + "&groupStatsPeriod=auto"} canSelectGroups={false} renderEmptyMessage={this.renderEmptyMessage} withChart withPagination={false} useFilteredStats customStatsPeriod={timePeriod} useTintRow={false}/>
        </TableWrapper>
      </react_1.Fragment>);
    };
    return RelatedIssues;
}(react_1.Component));
var StyledSectionHeading = styled_1.default(styles_1.SectionHeading)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var ControlsWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var TableWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space_1.default(4), panels_1.Panel, space_1.default(1));
exports.default = RelatedIssues;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=relatedIssues.jsx.map