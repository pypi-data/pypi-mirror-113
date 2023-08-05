Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var dropdownControl_1 = tslib_1.__importDefault(require("app/components/dropdownControl"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var subscribeButton_1 = tslib_1.__importDefault(require("app/components/subscribeButton"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dates_1 = require("app/utils/dates");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var types_1 = require("app/views/alerts/incidentRules/types");
var status_1 = tslib_1.__importDefault(require("../status"));
var utils_1 = require("../utils");
var DetailsHeader = /** @class */ (function (_super) {
    tslib_1.__extends(DetailsHeader, _super);
    function DetailsHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailsHeader.prototype.renderStatus = function () {
        var _a = this.props, incident = _a.incident, onStatusChange = _a.onStatusChange;
        var isIncidentOpen = incident && utils_1.isOpen(incident);
        var statusLabel = incident ? <StyledStatus incident={incident}/> : null;
        return (<dropdownControl_1.default data-test-id="status-dropdown" label={statusLabel} alignRight blendWithActor={false} buttonProps={{
                size: 'small',
                disabled: !incident || !isIncidentOpen,
                hideBottomBorder: false,
            }}>
        <StatusMenuItem isActive>
          {incident && <status_1.default disableIconColor incident={incident}/>}
        </StatusMenuItem>
        <StatusMenuItem onSelect={onStatusChange}>
          <icons_1.IconCheckmark color="green300"/>
          {locale_1.t('Resolved')}
        </StatusMenuItem>
      </dropdownControl_1.default>);
    };
    DetailsHeader.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, hasIncidentDetailsError = _d.hasIncidentDetailsError, incident = _d.incident, params = _d.params, stats = _d.stats, onSubscriptionChange = _d.onSubscriptionChange;
        var isIncidentReady = !!incident && !hasIncidentDetailsError;
        // ex - Wed, May 27, 2020 11:09 AM
        var dateFormat = dates_1.use24Hours() ? 'ddd, MMM D, YYYY HH:mm' : 'llll';
        var dateStarted = incident && moment_1.default(new Date(incident.dateStarted)).format(dateFormat);
        var duration = incident &&
            moment_1.default(incident.dateClosed ? new Date(incident.dateClosed) : new Date()).diff(moment_1.default(new Date(incident.dateStarted)), 'seconds');
        var isErrorDataset = ((_a = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _a === void 0 ? void 0 : _a.dataset) === types_1.Dataset.ERRORS;
        var environmentLabel = (_c = (_b = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _b === void 0 ? void 0 : _b.environment) !== null && _c !== void 0 ? _c : locale_1.t('All Environments');
        var project = incident && incident.projects && incident.projects[0];
        return (<Header>
        <BreadCrumbBar>
          <AlertBreadcrumbs crumbs={[
                { label: locale_1.t('Alerts'), to: "/organizations/" + params.orgId + "/alerts/" },
                { label: incident && "#" + incident.id },
            ]}/>
          <Controls>
            <subscribeButton_1.default disabled={!isIncidentReady} isSubscribed={incident === null || incident === void 0 ? void 0 : incident.isSubscribed} onClick={onSubscriptionChange} size="small"/>
            {this.renderStatus()}
          </Controls>
        </BreadCrumbBar>
        <Details columns={isErrorDataset ? 5 : 3}>
          <div>
            <IncidentTitle data-test-id="incident-title" loading={!isIncidentReady}>
              {incident && !hasIncidentDetailsError ? incident.title : 'Loading'}
            </IncidentTitle>
            <IncidentSubTitle loading={!isIncidentReady}>
              {locale_1.t('Triggered: ')}
              {dateStarted}
            </IncidentSubTitle>
          </div>

          {hasIncidentDetailsError ? (<StyledLoadingError />) : (<GroupedHeaderItems columns={isErrorDataset ? 5 : 3}>
              <ItemTitle>{locale_1.t('Environment')}</ItemTitle>
              <ItemTitle>{locale_1.t('Project')}</ItemTitle>
              {isErrorDataset && <ItemTitle>{locale_1.t('Users affected')}</ItemTitle>}
              {isErrorDataset && <ItemTitle>{locale_1.t('Total events')}</ItemTitle>}
              <ItemTitle>{locale_1.t('Active For')}</ItemTitle>
              <ItemValue>{environmentLabel}</ItemValue>
              <ItemValue>
                {project ? (<projects_1.default slugs={[project]} orgId={params.orgId}>
                    {function (_a) {
                        var projects = _a.projects;
                        return (projects === null || projects === void 0 ? void 0 : projects.length) && (<projectBadge_1.default avatarSize={18} project={projects[0]}/>);
                    }}
                  </projects_1.default>) : (<placeholder_1.default height="25px"/>)}
              </ItemValue>
              {isErrorDataset && (<ItemValue>
                  {stats ? (<count_1.default value={stats.uniqueUsers}/>) : (<placeholder_1.default height="25px"/>)}
                </ItemValue>)}
              {isErrorDataset && (<ItemValue>
                  {stats ? (<count_1.default value={stats.totalEvents}/>) : (<placeholder_1.default height="25px"/>)}
                </ItemValue>)}
              <ItemValue>
                {incident ? (<duration_1.default seconds={getDynamicText_1.default({ value: duration || 0, fixed: 1200 })}/>) : (<placeholder_1.default height="25px"/>)}
              </ItemValue>
            </GroupedHeaderItems>)}
        </Details>
      </Header>);
    };
    return DetailsHeader;
}(React.Component));
exports.default = DetailsHeader;
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
var BreadCrumbBar = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"], ["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"])), space_1.default(2), space_1.default(4), space_1.default(1));
var AlertBreadcrumbs = styled_1.default(breadcrumbs_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"], ["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var Controls = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space_1.default(1));
var Details = styled_1.default(organization_1.PageHeader, {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'columns'; },
})(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"])), space_1.default(1.5), space_1.default(4), space_1.default(2), space_1.default(3), function (p) { return p.theme.breakpoints[p.columns === 3 ? 1 : 2]; });
var StyledLoadingError = styled_1.default(loadingError_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n\n  &.alert.alert-block {\n    margin: 0 20px;\n  }\n"], ["\n  flex: 1;\n\n  &.alert.alert-block {\n    margin: 0 20px;\n  }\n"])));
var GroupedHeaderItems = styled_1.default('div', {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'columns'; },
})(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", " ", ";\n  text-align: right;\n  margin-top: ", ";\n\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", " ", ";\n  text-align: right;\n  margin-top: ", ";\n\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"])), function (p) { return p.columns; }, space_1.default(1), space_1.default(4), space_1.default(1), function (p) { return p.theme.breakpoints[p.columns === 3 ? 1 : 2]; });
var ItemTitle = styled_1.default('h6')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: 0;\n  text-transform: uppercase;\n  color: ", ";\n  letter-spacing: 0.1px;\n"], ["\n  font-size: ", ";\n  margin-bottom: 0;\n  text-transform: uppercase;\n  color: ", ";\n  letter-spacing: 0.1px;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var ItemValue = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var IncidentTitle = styled_1.default(pageHeading_1.default, {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'loading'; },
})(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  ", ";\n  line-height: 1.5;\n"], ["\n  ", ";\n  line-height: 1.5;\n"])), function (p) { return p.loading && 'opacity: 0'; });
var IncidentSubTitle = styled_1.default('div', {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'loading'; },
})(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  ", ";\n  font-size: ", ";\n  color: ", ";\n"], ["\n  ", ";\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.loading && 'opacity: 0'; }, function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray300; });
var StyledStatus = styled_1.default(status_1.default)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(2));
var StatusMenuItem = styled_1.default(menuItem_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  > span {\n    padding: ", " ", ";\n    font-size: ", ";\n    font-weight: 600;\n    line-height: 1;\n    text-align: left;\n    display: grid;\n    grid-template-columns: max-content 1fr;\n    grid-gap: ", ";\n    align-items: center;\n  }\n"], ["\n  > span {\n    padding: ", " ", ";\n    font-size: ", ";\n    font-weight: 600;\n    line-height: 1;\n    text-align: left;\n    display: grid;\n    grid-template-columns: max-content 1fr;\n    grid-gap: ", ";\n    align-items: center;\n  }\n"])), space_1.default(1), space_1.default(1.5), function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.75));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=header.jsx.map