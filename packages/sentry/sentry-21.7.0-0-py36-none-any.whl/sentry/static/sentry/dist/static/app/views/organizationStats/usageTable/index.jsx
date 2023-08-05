Object.defineProperty(exports, "__esModule", { value: true });
exports.CellSetting = exports.CellProject = exports.CellStat = exports.StyledPanelTable = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var headerItem_1 = require("app/components/organizations/headerItem");
var panels_1 = require("app/components/panels");
var panelTable_1 = tslib_1.__importDefault(require("app/components/panels/panelTable"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var utils_1 = require("../utils");
var DOCS_URL = 'https://docs.sentry.io/product/accounts/membership/#restricting-access';
var UsageTable = /** @class */ (function (_super) {
    tslib_1.__extends(UsageTable, _super);
    function UsageTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getErrorMessage = function (errorMessage) {
            if (errorMessage.projectStats.responseJSON.detail === 'No projects available') {
                return (<emptyMessage_1.default icon={<icons_1.IconWarning color="gray300" size="48"/>} title={locale_1.t("You don't have access to any projects, or your organization has no projects.")} description={locale_1.tct('Learn more about [link:Project Access]', {
                        link: <externalLink_1.default href={DOCS_URL}/>,
                    })}/>);
            }
            return <icons_1.IconWarning color="gray300" size="48"/>;
        };
        return _this;
    }
    Object.defineProperty(UsageTable.prototype, "formatUsageOptions", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            return {
                isAbbreviated: dataCategory !== types_1.DataCategory.ATTACHMENTS,
                useUnitScaling: dataCategory === types_1.DataCategory.ATTACHMENTS,
            };
        },
        enumerable: false,
        configurable: true
    });
    UsageTable.prototype.renderTableRow = function (stat) {
        var dataCategory = this.props.dataCategory;
        var project = stat.project, total = stat.total, accepted = stat.accepted, filtered = stat.filtered, dropped = stat.dropped;
        return [
            <exports.CellProject key={0}>
        <link_1.default to={stat.projectLink}>
          <StyledIdBadge avatarSize={16} disableLink hideOverflow project={project} displayName={project.slug}/>
        </link_1.default>
        <headerItem_1.SettingsIconLink to={stat.projectSettingsLink}>
          <icons_1.IconSettings size={theme_1.default.iconSizes.sm}/>
        </headerItem_1.SettingsIconLink>
      </exports.CellProject>,
            <exports.CellStat key={1}>
        {utils_1.formatUsageWithUnits(total, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
            <exports.CellStat key={2}>
        {utils_1.formatUsageWithUnits(accepted, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
            <exports.CellStat key={3}>
        {utils_1.formatUsageWithUnits(filtered, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
            <exports.CellStat key={4}>
        {utils_1.formatUsageWithUnits(dropped, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
        ];
    };
    UsageTable.prototype.render = function () {
        var _this = this;
        var _a = this.props, isEmpty = _a.isEmpty, isLoading = _a.isLoading, isError = _a.isError, errors = _a.errors, headers = _a.headers, usageStats = _a.usageStats;
        if (isError) {
            return (<panels_1.Panel>
          <errorPanel_1.default height="256px">{this.getErrorMessage(errors)}</errorPanel_1.default>
        </panels_1.Panel>);
        }
        return (<exports.StyledPanelTable isLoading={isLoading} isEmpty={isEmpty} headers={headers}>
        {usageStats.map(function (s) { return _this.renderTableRow(s); })}
      </exports.StyledPanelTable>);
    };
    return UsageTable;
}(React.Component));
exports.default = UsageTable;
exports.StyledPanelTable = styled_1.default(panelTable_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(5, auto);\n\n  @media (min-width: ", ") {\n    grid-template-columns: auto repeat(4, 100px);\n  }\n"], ["\n  grid-template-columns: repeat(5, auto);\n\n  @media (min-width: ", ") {\n    grid-template-columns: auto repeat(4, 100px);\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
exports.CellStat = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 1;\n  text-align: right;\n"], ["\n  flex-shrink: 1;\n  text-align: right;\n"])));
exports.CellProject = styled_1.default(exports.CellStat)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"], ["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"])));
exports.CellSetting = styled_1.default(exports.CellStat)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: 0;\n"])));
var StyledIdBadge = styled_1.default(idBadge_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"], ["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map