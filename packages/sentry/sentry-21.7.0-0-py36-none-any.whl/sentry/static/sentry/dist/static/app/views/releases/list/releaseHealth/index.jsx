Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var content_1 = tslib_1.__importDefault(require("./content"));
var ReleaseHealth = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseHealth, _super);
    function ReleaseHealth() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ReleaseHealth.prototype.shouldComponentUpdate = function (nextProps) {
        // we don't want project health rows to reorder/jump while the whole card is loading
        if (this.props.reloading && nextProps.reloading) {
            return false;
        }
        return true;
    };
    ReleaseHealth.prototype.render = function () {
        var _a = this.props, release = _a.release, organization = _a.organization, activeDisplay = _a.activeDisplay, location = _a.location, showPlaceholders = _a.showPlaceholders, selection = _a.selection, isTopRelease = _a.isTopRelease, getHealthData = _a.getHealthData;
        // sort health rows inside release card alphabetically by project name,
        // show only the ones that are selected in global header
        var _b = tslib_1.__read(partition_1.default(release.projects.sort(function (a, b) { return a.slug.localeCompare(b.slug); }), function (p) {
            // do not filter for My Projects & All Projects
            return selection.projects.length > 0 && !selection.projects.includes(-1)
                ? selection.projects.includes(p.id)
                : true;
        }), 2), projectsToShow = _b[0], projectsToHide = _b[1];
        function getHiddenProjectsTooltip() {
            var limitedProjects = projectsToHide.map(function (p) { return p.slug; }).slice(0, 5);
            var remainderLength = projectsToHide.length - limitedProjects.length;
            if (remainderLength) {
                limitedProjects.push(locale_1.tn('and %s more', 'and %s more', remainderLength));
            }
            return limitedProjects.join(', ');
        }
        return (<react_1.Fragment>
        <content_1.default organization={organization} activeDisplay={activeDisplay} releaseVersion={release.version} showAdoptionStageLabels={selection.environments.length === 1} adoptionStages={release.adoptionStages} projects={projectsToShow} location={location} showPlaceholders={showPlaceholders} isTopRelease={isTopRelease} getHealthData={getHealthData}/>

        {projectsToHide.length > 0 && (<HiddenProjectsMessage>
            <tooltip_1.default title={getHiddenProjectsTooltip()}>
              <textOverflow_1.default>
                {projectsToHide.length === 1
                    ? locale_1.tct('[number:1] hidden project', { number: <strong /> })
                    : locale_1.tct('[number] hidden projects', {
                        number: <strong>{projectsToHide.length}</strong>,
                    })}
              </textOverflow_1.default>
            </tooltip_1.default>
          </HiddenProjectsMessage>)}
      </react_1.Fragment>);
    };
    return ReleaseHealth;
}(react_1.Component));
var HiddenProjectsMessage = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n  padding: 0 ", ";\n  border-top: 1px solid ", ";\n  overflow: hidden;\n  height: 24px;\n  line-height: 24px;\n  color: ", ";\n  background-color: ", ";\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n  padding: 0 ", ";\n  border-top: 1px solid ", ";\n  overflow: hidden;\n  height: 24px;\n  line-height: 24px;\n  color: ", ";\n  background-color: ", ";\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.borderRadius; });
exports.default = ReleaseHealth;
var templateObject_1;
//# sourceMappingURL=index.jsx.map