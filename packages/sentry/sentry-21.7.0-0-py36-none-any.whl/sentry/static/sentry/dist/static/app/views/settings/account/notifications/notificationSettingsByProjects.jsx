Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var constants_1 = require("app/views/settings/account/notifications/constants");
var utils_2 = require("app/views/settings/account/notifications/utils");
var defaultSearchBar_1 = require("app/views/settings/components/defaultSearchBar");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var NotificationSettingsByProjects = /** @class */ (function (_super) {
    tslib_1.__extends(NotificationSettingsByProjects, _super);
    function NotificationSettingsByProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getProjectCount = function () {
            var _a;
            /** Check the notification settings for how many projects there are. */
            var _b = _this.props, notificationType = _b.notificationType, notificationSettings = _b.notificationSettings;
            return Object.values(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a.project) || {}).length;
        };
        _this.getGroupedProjects = function () {
            /**
             * The UI expects projects to be grouped by organization but can also use
             * this function to make a single group with all organizations.
             */
            var stateProjects = _this.state.projects;
            return Object.fromEntries(Object.values(utils_2.groupByOrganization(utils_1.sortProjects(stateProjects))).map(function (_a) {
                var organization = _a.organization, projects = _a.projects;
                return [organization.name + " Projects", projects];
            }));
        };
        return _this;
    }
    NotificationSettingsByProjects.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { projects: [] });
    };
    NotificationSettingsByProjects.prototype.getEndpoints = function () {
        return [['projects', '/projects/']];
    };
    NotificationSettingsByProjects.prototype.renderBody = function () {
        var _a = this.props, notificationType = _a.notificationType, notificationSettings = _a.notificationSettings, onChange = _a.onChange;
        var _b = this.state, projects = _b.projects, projectsPageLinks = _b.projectsPageLinks;
        var canSearch = this.getProjectCount() >= constants_1.MIN_PROJECTS_FOR_SEARCH;
        var shouldPaginate = projects.length >= constants_1.MIN_PROJECTS_FOR_PAGINATION;
        // eslint-disable-next-line react/prop-types
        var renderSearch = function (_a) {
            var defaultSearchBar = _a.defaultSearchBar;
            return (<StyledSearchWrapper>{defaultSearchBar}</StyledSearchWrapper>);
        };
        return (<react_1.default.Fragment>
        {canSearch &&
                this.renderSearchInput({
                    stateKey: 'projects',
                    url: '/projects/',
                    placeholder: locale_1.t('Search Projects'),
                    children: renderSearch,
                })}
        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={utils_2.getParentData(notificationType, notificationSettings, projects)}>
          {projects.length === 0 ? (<emptyMessage_1.default>{locale_1.t('No projects found')}</emptyMessage_1.default>) : (Object.entries(this.getGroupedProjects()).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), groupTitle = _b[0], parents = _b[1];
                return (<jsonForm_1.default key={groupTitle} title={groupTitle} fields={parents.map(function (parent) {
                        return utils_2.getParentField(notificationType, notificationSettings, parent, onChange);
                    })}/>);
            }))}
        </form_1.default>
        {canSearch && shouldPaginate && (<pagination_1.default pageLinks={projectsPageLinks} {...this.props}/>)}
      </react_1.default.Fragment>);
    };
    return NotificationSettingsByProjects;
}(asyncComponent_1.default));
exports.default = NotificationSettingsByProjects;
var StyledSearchWrapper = styled_1.default(defaultSearchBar_1.SearchWrapper)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  * {\n    width: 100%;\n  }\n"], ["\n  * {\n    width: 100%;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=notificationSettingsByProjects.jsx.map