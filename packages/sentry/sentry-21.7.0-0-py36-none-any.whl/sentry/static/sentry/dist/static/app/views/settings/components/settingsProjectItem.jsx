Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var bookmarkStar_1 = tslib_1.__importDefault(require("app/components/projects/bookmarkStar"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ProjectItem = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectItem, _super);
    function ProjectItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isBookmarked: _this.props.project.isBookmarked,
        };
        _this.handleToggleBookmark = function (isBookmarked) {
            _this.setState({ isBookmarked: isBookmarked });
        };
        return _this;
    }
    ProjectItem.prototype.render = function () {
        var _a = this.props, project = _a.project, organization = _a.organization;
        return (<Wrapper>
        <BookmarkLink organization={organization} project={project} isBookmarked={this.state.isBookmarked} onToggle={this.handleToggleBookmark}/>
        <projectBadge_1.default to={"/settings/" + organization.slug + "/projects/" + project.slug + "/"} avatarSize={18} project={project}/>
      </Wrapper>);
    };
    return ProjectItem;
}(react_1.Component));
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var BookmarkLink = styled_1.default(bookmarkStar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  margin-top: -", ";\n"], ["\n  margin-right: ", ";\n  margin-top: -", ";\n"])), space_1.default(1), space_1.default(0.25));
exports.default = ProjectItem;
var templateObject_1, templateObject_2;
//# sourceMappingURL=settingsProjectItem.jsx.map