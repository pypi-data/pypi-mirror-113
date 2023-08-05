Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var unknownUser = {
    id: '',
    name: '',
    username: '??',
    email: '',
    avatarUrl: '',
    avatar: {
        avatarUuid: '',
        avatarType: 'letter_avatar',
    },
    ip_address: '',
};
var LastCommit = /** @class */ (function (_super) {
    tslib_1.__extends(LastCommit, _super);
    function LastCommit() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LastCommit.prototype.renderMessage = function (message) {
        if (!message) {
            return locale_1.t('No message provided');
        }
        var firstLine = message.split(/\n/)[0];
        if (firstLine.length > 100) {
            var truncated = firstLine.substr(0, 90);
            var words = truncated.split(/ /);
            // try to not have elipsis mid-word
            if (words.length > 1) {
                words.pop();
                truncated = words.join(' ');
            }
            return truncated + '...';
        }
        return firstLine;
    };
    LastCommit.prototype.render = function () {
        var _a = this.props, commit = _a.commit, headerClass = _a.headerClass;
        var commitAuthor = commit && commit.author;
        return (<div>
        <h6 className={headerClass}>Last commit</h6>
        <div className="commit">
          <div className="commit-avatar">
            <userAvatar_1.default user={commitAuthor || unknownUser}/>
          </div>
          <div className="commit-message truncate">
            {this.renderMessage(commit.message)}
          </div>
          <div className="commit-meta">
            <strong>{(commitAuthor && commitAuthor.name) || locale_1.t('Unknown Author')}</strong>
            &nbsp;
            <timeSince_1.default date={commit.dateCreated}/>
          </div>
        </div>
      </div>);
    };
    return LastCommit;
}(react_1.Component));
exports.default = LastCommit;
//# sourceMappingURL=lastCommit.jsx.map