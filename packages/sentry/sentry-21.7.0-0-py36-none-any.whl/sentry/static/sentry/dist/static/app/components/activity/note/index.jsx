Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var item_1 = tslib_1.__importDefault(require("app/components/activity/item"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var body_1 = tslib_1.__importDefault(require("./body"));
var editorTools_1 = tslib_1.__importDefault(require("./editorTools"));
var header_1 = tslib_1.__importDefault(require("./header"));
var input_1 = tslib_1.__importDefault(require("./input"));
var Note = /** @class */ (function (_super) {
    tslib_1.__extends(Note, _super);
    function Note() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            editing: false,
        };
        _this.handleEdit = function () {
            _this.setState({ editing: true });
        };
        _this.handleEditFinish = function () {
            _this.setState({ editing: false });
        };
        _this.handleDelete = function () {
            var onDelete = _this.props.onDelete;
            onDelete(_this.props);
        };
        _this.handleCreate = function (note) {
            var onCreate = _this.props.onCreate;
            if (onCreate) {
                onCreate(note);
            }
        };
        _this.handleUpdate = function (note) {
            var onUpdate = _this.props.onUpdate;
            onUpdate(note, _this.props);
            _this.setState({ editing: false });
        };
        return _this;
    }
    Note.prototype.render = function () {
        var _this = this;
        var _a = this.props, modelId = _a.modelId, user = _a.user, dateCreated = _a.dateCreated, text = _a.text, authorName = _a.authorName, hideDate = _a.hideDate, minHeight = _a.minHeight, showTime = _a.showTime, projectSlugs = _a.projectSlugs;
        var activityItemProps = {
            hideDate: hideDate,
            showTime: showTime,
            id: "activity-item-" + modelId,
            author: {
                type: 'user',
                user: user,
            },
            date: dateCreated,
        };
        if (!this.state.editing) {
            return (<ActivityItemWithEditing {...activityItemProps} header={<header_1.default authorName={authorName} user={user} onEdit={this.handleEdit} onDelete={this.handleDelete}/>}>
          <body_1.default text={text}/>
        </ActivityItemWithEditing>);
        }
        // When editing, `NoteInput` has its own header, pass render func
        // to control rendering of bubble body
        return (<StyledActivityItem {...activityItemProps}>
        {function () { return (<input_1.default modelId={modelId} minHeight={minHeight} text={text} onEditFinish={_this.handleEditFinish} onUpdate={_this.handleUpdate} onCreate={_this.handleCreate} projectSlugs={projectSlugs}/>); }}
      </StyledActivityItem>);
    };
    return Note;
}(react_1.Component));
var StyledActivityItem = styled_1.default(item_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /* this was nested under \".activity-note.activity-bubble\" */\n  ul {\n    list-style: disc;\n  }\n\n  h1,\n  h2,\n  h3,\n  h4,\n  p,\n  ul:not(.nav),\n  ol,\n  pre,\n  hr,\n  blockquote {\n    margin-bottom: ", ";\n  }\n\n  ul:not(.nav),\n  ol {\n    padding-left: 20px;\n  }\n\n  p {\n    a {\n      word-wrap: break-word;\n    }\n  }\n\n  blockquote {\n    font-size: 15px;\n    background: ", ";\n\n    p:last-child {\n      margin-bottom: 0;\n    }\n  }\n"], ["\n  /* this was nested under \".activity-note.activity-bubble\" */\n  ul {\n    list-style: disc;\n  }\n\n  h1,\n  h2,\n  h3,\n  h4,\n  p,\n  ul:not(.nav),\n  ol,\n  pre,\n  hr,\n  blockquote {\n    margin-bottom: ", ";\n  }\n\n  ul:not(.nav),\n  ol {\n    padding-left: 20px;\n  }\n\n  p {\n    a {\n      word-wrap: break-word;\n    }\n  }\n\n  blockquote {\n    font-size: 15px;\n    background: ", ";\n\n    p:last-child {\n      margin-bottom: 0;\n    }\n  }\n"])), space_1.default(2), function (p) { return p.theme.gray200; });
var ActivityItemWithEditing = styled_1.default(StyledActivityItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  &:hover {\n    ", " {\n      display: inline-block;\n    }\n  }\n"], ["\n  &:hover {\n    ", " {\n      display: inline-block;\n    }\n  }\n"])), editorTools_1.default);
exports.default = Note;
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map