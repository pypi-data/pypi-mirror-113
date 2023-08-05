Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var toolbarHeader_1 = tslib_1.__importDefault(require("app/components/toolbarHeader"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function Headers(_a) {
    var selection = _a.selection, statsPeriod = _a.statsPeriod, onSelectStatsPeriod = _a.onSelectStatsPeriod, isReprocessingQuery = _a.isReprocessingQuery;
    return (<react_1.Fragment>
      {isReprocessingQuery ? (<react_1.Fragment>
          <StartedColumn>{locale_1.t('Started')}</StartedColumn>
          <EventsReprocessedColumn>{locale_1.t('Events Reprocessed')}</EventsReprocessedColumn>
          <ProgressColumn>{locale_1.t('Progress')}</ProgressColumn>
        </react_1.Fragment>) : (<react_1.Fragment>
          <GraphHeaderWrapper className="hidden-xs hidden-sm hidden-md">
            <GraphHeader>
              <StyledToolbarHeader>{locale_1.t('Graph:')}</StyledToolbarHeader>
              {selection.datetime.period !== '24h' && (<GraphToggle active={statsPeriod === '24h'} onClick={function () { return onSelectStatsPeriod('24h'); }}>
                  {locale_1.t('24h')}
                </GraphToggle>)}
              <GraphToggle active={statsPeriod === 'auto'} onClick={function () { return onSelectStatsPeriod('auto'); }}>
                {selection.datetime.period || locale_1.t('Custom')}
              </GraphToggle>
            </GraphHeader>
          </GraphHeaderWrapper>
          <EventsOrUsersLabel>{locale_1.t('Events')}</EventsOrUsersLabel>
          <EventsOrUsersLabel>{locale_1.t('Users')}</EventsOrUsersLabel>
          <AssigneesLabel className="hidden-xs hidden-sm">
            <toolbarHeader_1.default>{locale_1.t('Assignee')}</toolbarHeader_1.default>
          </AssigneesLabel>
        </react_1.Fragment>)}
    </react_1.Fragment>);
}
exports.default = Headers;
var GraphHeaderWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n  animation: 0.25s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"], ["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n  animation: 0.25s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"])), space_1.default(2), space_1.default(2));
var GraphHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledToolbarHeader = styled_1.default(toolbarHeader_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var GraphToggle = styled_1.default('a')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 13px;\n  padding-left: ", ";\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  font-size: 13px;\n  padding-left: ", ";\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), space_1.default(1), function (p) { return (p.active ? p.theme.textColor : p.theme.disabled); });
var EventsOrUsersLabel = styled_1.default(toolbarHeader_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  align-items: center;\n  justify-content: flex-end;\n  text-align: right;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  display: inline-grid;\n  align-items: center;\n  justify-content: flex-end;\n  text-align: right;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[3]; });
var AssigneesLabel = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"], ["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"])), space_1.default(2), space_1.default(2));
// Reprocessing
var StartedColumn = styled_1.default(toolbarHeader_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"], ["\n  margin: 0 ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"])), space_1.default(2), overflowEllipsis_1.default, function (p) { return p.theme.breakpoints[0]; });
var EventsReprocessedColumn = styled_1.default(toolbarHeader_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"], ["\n  margin: 0 ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"])), space_1.default(2), overflowEllipsis_1.default, function (p) { return p.theme.breakpoints[0]; });
var ProgressColumn = styled_1.default(toolbarHeader_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"], ["\n  margin: 0 ", ";\n\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=headers.jsx.map