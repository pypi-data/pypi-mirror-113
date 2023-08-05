Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sortBy_1 = tslib_1.__importDefault(require("lodash/sortBy"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var selectorItem_1 = tslib_1.__importDefault(require("./selectorItem"));
var ProjectSelector = function (_a) {
    var children = _a.children, organization = _a.organization, menuFooter = _a.menuFooter, className = _a.className, rootClassName = _a.rootClassName, onClose = _a.onClose, onFilterChange = _a.onFilterChange, onScroll = _a.onScroll, searching = _a.searching, paginated = _a.paginated, multiProjects = _a.multiProjects, onSelect = _a.onSelect, onMultiSelect = _a.onMultiSelect, _b = _a.multi, multi = _b === void 0 ? false : _b, _c = _a.selectedProjects, selectedProjects = _c === void 0 ? [] : _c, props = tslib_1.__rest(_a, ["children", "organization", "menuFooter", "className", "rootClassName", "onClose", "onFilterChange", "onScroll", "searching", "paginated", "multiProjects", "onSelect", "onMultiSelect", "multi", "selectedProjects"]);
    var getProjects = function () {
        var _a = props.nonMemberProjects, nonMemberProjects = _a === void 0 ? [] : _a;
        return [
            sortBy_1.default(multiProjects, function (project) { return [
                !selectedProjects.find(function (selectedProject) { return selectedProject.slug === project.slug; }),
                !project.isBookmarked,
                project.slug,
            ]; }),
            sortBy_1.default(nonMemberProjects, function (project) { return [project.slug]; }),
        ];
    };
    var _d = tslib_1.__read(getProjects(), 2), projects = _d[0], nonMemberProjects = _d[1];
    var handleSelect = function (_a) {
        var project = _a.value;
        onSelect(project);
    };
    var handleMultiSelect = function (project, event) {
        if (!onMultiSelect) {
            // eslint-disable-next-line no-console
            console.error('ProjectSelector is a controlled component but `onMultiSelect` callback is not defined');
            return;
        }
        var selectedProjectsMap = new Map(selectedProjects.map(function (p) { return [p.slug, p]; }));
        if (selectedProjectsMap.has(project.slug)) {
            // unselected a project
            selectedProjectsMap.delete(project.slug);
            onMultiSelect(Array.from(selectedProjectsMap.values()), event);
            return;
        }
        selectedProjectsMap.set(project.slug, project);
        onMultiSelect(Array.from(selectedProjectsMap.values()), event);
    };
    var getProjectItem = function (project) { return ({
        value: project,
        searchKey: project.slug,
        label: function (_a) {
            var inputValue = _a.inputValue;
            return (<selectorItem_1.default project={project} organization={organization} multi={multi} inputValue={inputValue} isChecked={!!selectedProjects.find(function (_a) {
                var slug = _a.slug;
                return slug === project.slug;
            })} onMultiSelect={handleMultiSelect}/>);
        },
    }); };
    var getItems = function (hasProjects) {
        if (!hasProjects) {
            return [];
        }
        return [
            {
                hideGroupLabel: true,
                items: projects.map(getProjectItem),
            },
            {
                hideGroupLabel: nonMemberProjects.length === 0,
                itemSize: 'small',
                id: 'no-membership-header',
                label: <Label>{locale_1.t("Projects I don't belong to")}</Label>,
                items: nonMemberProjects.map(getProjectItem),
            },
        ];
    };
    var hasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length) || !!(nonMemberProjects === null || nonMemberProjects === void 0 ? void 0 : nonMemberProjects.length);
    var newProjectUrl = "/organizations/" + organization.slug + "/projects/new/";
    var hasProjectWrite = organization.access.includes('project:write');
    return (<dropdownAutoComplete_1.default blendCorner={false} searchPlaceholder={locale_1.t('Filter projects')} onSelect={handleSelect} onClose={onClose} onChange={onFilterChange} busyItemsStillVisible={searching} onScroll={onScroll} maxHeight={500} inputProps={{ style: { padding: 8, paddingLeft: 10 } }} rootClassName={rootClassName} className={className} emptyMessage={locale_1.t('You have no projects')} noResultsMessage={locale_1.t('No projects found')} virtualizedHeight={theme_1.default.headerSelectorRowHeight} virtualizedLabelHeight={theme_1.default.headerSelectorLabelHeight} emptyHidesInput={!paginated} inputActions={<AddButton disabled={!hasProjectWrite} to={newProjectUrl} size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>} title={!hasProjectWrite ? locale_1.t("You don't have permission to add a project") : undefined}>
          {locale_1.t('Project')}
        </AddButton>} menuFooter={function (renderProps) {
            var renderedFooter = typeof menuFooter === 'function' ? menuFooter(renderProps) : menuFooter;
            var showCreateProjectButton = !hasProjects && hasProjectWrite;
            if (!renderedFooter && !showCreateProjectButton) {
                return null;
            }
            return (<React.Fragment>
            {showCreateProjectButton && (<CreateProjectButton priority="primary" size="small" to={newProjectUrl}>
                {locale_1.t('Create project')}
              </CreateProjectButton>)}
            {renderedFooter}
          </React.Fragment>);
        }} items={getItems(hasProjects)} allowActorToggle closeOnSelect>
      {function (renderProps) { return children(tslib_1.__assign(tslib_1.__assign({}, renderProps), { selectedProjects: selectedProjects })); }}
    </dropdownAutoComplete_1.default>);
};
exports.default = ProjectSelector;
var Label = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var AddButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  margin: 0 ", ";\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  display: block;\n  margin: 0 ", ";\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), space_1.default(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.subText; });
var CreateProjectButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: block;\n  text-align: center;\n  margin: ", " 0;\n"], ["\n  display: block;\n  text-align: center;\n  margin: ", " 0;\n"])), space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map