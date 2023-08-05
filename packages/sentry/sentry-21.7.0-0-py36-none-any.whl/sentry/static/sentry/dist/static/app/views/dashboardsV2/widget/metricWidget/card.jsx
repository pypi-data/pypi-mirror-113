Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var chart_1 = tslib_1.__importDefault(require("./chart"));
var statsRequest_1 = tslib_1.__importDefault(require("./statsRequest"));
function Card(_a) {
    var widget = _a.widget, api = _a.api, location = _a.location, router = _a.router, organization = _a.organization, project = _a.project, selection = _a.selection;
    var groupings = widget.groupings, searchQuery = widget.searchQuery, title = widget.title, displayType = widget.displayType;
    return (<errorBoundary_1.default customComponent={<ErrorCard>{locale_1.t('Error loading widget data')}</ErrorCard>}>
      <StyledPanel>
        <Title>{title}</Title>
        <statsRequest_1.default api={api} location={location} organization={organization} projectSlug={project.slug} groupings={groupings} searchQuery={searchQuery} environments={selection.environments} datetime={selection.datetime}>
          {function (_a) {
            var isLoading = _a.isLoading, errored = _a.errored, series = _a.series;
            return (<chart_1.default displayType={displayType} series={series} isLoading={isLoading} errored={errored} location={location} platform={project.platform} selection={selection} router={router}/>);
        }}
        </statsRequest_1.default>
      </StyledPanel>
    </errorBoundary_1.default>);
}
exports.default = Card;
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n  padding: ", " ", ";\n"], ["\n  margin: 0;\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n  padding: ", " ", ";\n"])), space_1.default(2), space_1.default(3));
var ErrorCard = styled_1.default(placeholder_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.alert.error.border; }, function (p) { return p.theme.alert.error.textLight; }, function (p) { return p.theme.borderRadius; }, space_1.default(2));
var Title = styled_1.default(styles_1.HeaderTitle)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=card.jsx.map