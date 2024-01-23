import { createBoard } from '@wixc3/react-board';
import image from './'

export default createBoard({
    name: 'image card',
    Board: () => <div></div>,
    isSnippet: true,
    environmentProps: {
windowWidth: 1024,
windowHeight: 768
}
});
